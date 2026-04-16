"""Tests for ErrorHandler module."""

from unittest.mock import patch

import pytest
from datetime import datetime

from garage_os.runtime.error_handler import ErrorHandler, RetryStrategy, ErrorLogEntry
from garage_os.types import ErrorCategory


class TestErrorClassification:
    """Test error classification logic."""

    def test_classify_connection_error(self):
        """ConnectionError should be classified as RETRYABLE."""
        error = ConnectionError("Connection failed")
        category = ErrorHandler.classify_error(error)
        assert category == ErrorCategory.RETRYABLE

    def test_classify_timeout_error(self):
        """TimeoutError should be classified as RETRYABLE."""
        error = TimeoutError("Operation timed out")
        category = ErrorHandler.classify_error(error)
        assert category == ErrorCategory.RETRYABLE

    def test_classify_os_error(self):
        """OSError should be classified as RETRYABLE."""
        error = OSError("System error")
        category = ErrorHandler.classify_error(error)
        assert category == ErrorCategory.RETRYABLE

    def test_classify_permission_error(self):
        """PermissionError should be classified as USER_INTERVENTION."""
        error = PermissionError("Access denied")
        category = ErrorHandler.classify_error(error)
        assert category == ErrorCategory.USER_INTERVENTION

    def test_classify_file_not_found(self):
        """FileNotFoundError should be classified as USER_INTERVENTION."""
        error = FileNotFoundError("File not found")
        category = ErrorHandler.classify_error(error)
        assert category == ErrorCategory.USER_INTERVENTION

    def test_classify_value_error(self):
        """ValueError should be classified as FATAL."""
        error = ValueError("Invalid value")
        category = ErrorHandler.classify_error(error)
        assert category == ErrorCategory.FATAL

    def test_classify_json_decode_error(self):
        """JSONDecodeError should be classified as FATAL."""
        # JSONDecodeError is a subclass of ValueError with 'JSON' in the name
        import json

        error = json.JSONDecodeError("Expecting value", "test", 0)
        category = ErrorHandler.classify_error(error)
        assert category == ErrorCategory.FATAL

    def test_classify_unicode_error(self):
        """UnicodeDecodeError should be classified as FATAL."""
        error = UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid start byte")
        category = ErrorHandler.classify_error(error)
        assert category == ErrorCategory.FATAL


class TestRetryStrategy:
    """Test retry strategy generation."""

    def test_retry_strategy_retryable(self):
        """RETRYABLE category should return strategy with max_retries=3 and delays=[1,2,4]."""
        strategy = ErrorHandler.get_retry_strategy(ErrorCategory.RETRYABLE)
        assert strategy.max_retries == 3
        assert strategy.delays == [1.0, 2.0, 4.0]
        assert strategy.pause is False
        assert strategy.notify_user is False
        assert strategy.stop is False

    def test_retry_strategy_user_intervention(self):
        """USER_INTERVENTION category should return strategy with pause=True."""
        strategy = ErrorHandler.get_retry_strategy(ErrorCategory.USER_INTERVENTION)
        assert strategy.pause is True
        assert strategy.notify_user is True
        assert strategy.max_retries == 0
        assert strategy.delays == []

    def test_retry_strategy_fatal(self):
        """FATAL category should return strategy with stop=True."""
        strategy = ErrorHandler.get_retry_strategy(ErrorCategory.FATAL)
        assert strategy.stop is True
        assert strategy.log_fatal is True
        assert strategy.max_retries == 0

    def test_retry_strategy_ignorable(self):
        """IGNORABLE category should return strategy with continue_execution=True."""
        strategy = ErrorHandler.get_retry_strategy(ErrorCategory.IGNORABLE)
        assert strategy.continue_execution is True
        assert strategy.log is True
        assert strategy.max_retries == 0


class TestErrorLogging:
    """Test error logging functionality."""

    def test_log_error(self):
        """Error logging should create ErrorLogEntry with correct fields."""
        error = ValueError("Test error")
        category = ErrorCategory.FATAL
        session_id = "test-session-123"

        entry = ErrorHandler.log_error(error, category, session_id)

        assert isinstance(entry, ErrorLogEntry)
        assert entry.error_type == "ValueError"
        assert entry.message == "Test error"
        assert entry.category == ErrorCategory.FATAL
        assert entry.session_id == "test-session-123"
        assert entry.context is None
        assert isinstance(entry.timestamp, datetime)
        assert isinstance(entry.error_id, str)
        assert len(entry.error_id) > 0

    def test_log_error_with_context(self):
        """Error logging with context should record context information."""
        error = RuntimeError("Runtime failure")
        category = ErrorCategory.RETRYABLE
        session_id = "test-session-456"
        context = {"node_id": "node-1", "attempt": 2}

        entry = ErrorHandler.log_error(error, category, session_id, context)

        assert entry.context == context
        assert entry.context["node_id"] == "node-1"
        assert entry.context["attempt"] == 2

    def test_log_error_generates_unique_ids(self):
        """Each error log entry should have a unique error_id."""
        error = Exception("Test error")
        category = ErrorCategory.IGNORABLE

        entry1 = ErrorHandler.log_error(error, category)
        entry2 = ErrorHandler.log_error(error, category)

        assert entry1.error_id != entry2.error_id

    def test_log_error_strategy_matches_category(self):
        """Error log entry should have strategy matching its category."""
        error = ConnectionError("Connection failed")
        category = ErrorCategory.RETRYABLE

        entry = ErrorHandler.log_error(error, category)

        assert entry.strategy.max_retries == 3
        assert entry.strategy.delays == [1.0, 2.0, 4.0]


class TestExecuteWithRetry:
    """Test execute_with_retry functionality."""

    def test_successful_operation(self):
        """Successful operation should return result without retry."""
        def successful_op():
            return "success"

        result, error_entry = ErrorHandler.execute_with_retry(successful_op)

        assert result == "success"
        assert error_entry is None

    def test_retryable_retries_once(self):
        """RETRYABLE error should retry once and succeed."""
        attempt_count = [0]

        def flaky_op():
            attempt_count[0] += 1
            if attempt_count[0] == 1:
                raise ConnectionError("Connection failed")
            return "success"

        result, error_entry = ErrorHandler.execute_with_retry(flaky_op)

        assert result == "success"
        assert error_entry is None
        assert attempt_count[0] == 2

    def test_retryable_retries_exhausted(self):
        """RETRYABLE error should exhaust retries and upgrade to FATAL."""
        def always_failing_op():
            raise ConnectionError("Always fails")

        result, error_entry = ErrorHandler.execute_with_retry(
            always_failing_op, session_id="test-session"
        )

        assert result is None
        assert error_entry is not None
        assert error_entry.category == ErrorCategory.FATAL
        assert error_entry.session_id == "test-session"
        assert error_entry.error_type == "ConnectionError"

    def test_retry_delays_correct(self):
        """Retry delays should follow [1.0, 2.0, 4.0] pattern."""
        attempt_count = [0]
        delays_used = []

        def failing_op():
            attempt_count[0] += 1
            raise TimeoutError("Timeout")

        with patch("time.sleep") as mock_sleep:
            result, error_entry = ErrorHandler.execute_with_retry(failing_op)

            # Should have called sleep 3 times (for 3 retries)
            assert mock_sleep.call_count == 3

            # Check the delay values
            calls = [call.args[0] for call in mock_sleep.call_args_list]
            assert calls == [1.0, 2.0, 4.0]

    def test_user_intervention_no_retry(self):
        """USER_INTERVENTION error should not retry."""
        def permission_op():
            raise PermissionError("Access denied")

        result, error_entry = ErrorHandler.execute_with_retry(permission_op)

        assert result is None
        assert error_entry is not None
        assert error_entry.category == ErrorCategory.USER_INTERVENTION
        assert error_entry.strategy.pause is True

    def test_fatal_no_retry(self):
        """FATAL error should not retry."""
        def value_op():
            raise ValueError("Invalid value")

        result, error_entry = ErrorHandler.execute_with_retry(value_op)

        assert result is None
        assert error_entry is not None
        assert error_entry.category == ErrorCategory.FATAL
        assert error_entry.strategy.stop is True

    def test_ignorable_no_retry(self):
        """IGNORABLE error should not retry and continue execution."""
        def runtime_op():
            raise RuntimeError("Runtime issue")

        result, error_entry = ErrorHandler.execute_with_retry(runtime_op)

        assert result is None
        assert error_entry is not None
        assert error_entry.category == ErrorCategory.IGNORABLE
        assert error_entry.strategy.continue_execution is True


class TestErrorClassificationAdditional:
    """Additional tests for error classification."""

    def test_classify_runtime_error_as_ignorable(self):
        """RuntimeError should be classified as IGNORABLE."""
        error = RuntimeError("Runtime issue")
        category = ErrorHandler.classify_error(error)
        assert category == ErrorCategory.IGNORABLE

    def test_classify_key_error_as_ignorable(self):
        """KeyError should be classified as IGNORABLE."""
        error = KeyError("missing_key")
        category = ErrorHandler.classify_error(error)
        assert category == ErrorCategory.IGNORABLE

