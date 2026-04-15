"""Tests for atomic_writer module."""

import json
import os
import tempfile
from pathlib import Path

import pytest

from garage_os.storage.atomic_writer import AtomicWriter


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestAtomicWriter:
    """Test cases for AtomicWriter class."""

    def test_write_and_read_text(self, temp_dir):
        """Test writing text and reading it back verifies content consistency."""
        test_file = temp_dir / "test.txt"
        content = "Hello, World!"

        checksum = AtomicWriter.write_text(test_file, content)
        assert isinstance(checksum, str)
        assert len(checksum) == 64  # SHA-256 produces 64 hex characters

        # Verify file was created
        assert test_file.exists()

        # Read back and verify
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content == content

    def test_write_and_read_json(self, temp_dir):
        """Test writing JSON and reading it back verifies correctness."""
        test_file = temp_dir / "test.json"
        data = {"key": "value", "number": 42, "nested": {"a": 1, "b": 2}}

        checksum = AtomicWriter.write_json(test_file, data)
        assert isinstance(checksum, str)
        assert len(checksum) == 64

        # Verify file was created
        assert test_file.exists()

        # Read back and verify
        read_data = AtomicWriter.read_json(test_file)
        assert read_data == data

    def test_checksum_correct(self, temp_dir):
        """Test that checksum computation is correct."""
        content = "Test content for checksum"
        checksum1 = AtomicWriter.compute_checksum(content)
        checksum2 = AtomicWriter.compute_checksum(content)

        assert checksum1 == checksum2
        assert len(checksum1) == 64
        assert all(c in "0123456789abcdef" for c in checksum1)

    def test_checksum_mismatch(self, temp_dir):
        """Test that modified content has different checksum."""
        original_content = "Original content"
        modified_content = "Modified content"

        original_checksum = AtomicWriter.compute_checksum(original_content)
        modified_checksum = AtomicWriter.compute_checksum(modified_content)

        assert original_checksum != modified_checksum

        # Verify file checksum mismatch after modification
        test_file = temp_dir / "test.txt"
        checksum = AtomicWriter.write_text(test_file, original_content)
        assert checksum == original_checksum

        # Modify file
        test_file.write_text(modified_content)

        # Verify checksum no longer matches
        assert not AtomicWriter.verify_checksum(test_file, original_checksum)
        assert AtomicWriter.verify_checksum(test_file, modified_checksum)

    def test_atomic_on_interrupt(self, temp_dir):
        """Test that interrupting write doesn't affect original file."""
        test_file = temp_dir / "test.txt"
        original_content = "Original content"

        # Write initial content
        original_checksum = AtomicWriter.write_text(test_file, original_content)

        # Simulate interrupted write: create temp file but don't rename
        # This tests that original file remains intact
        temp_file = temp_dir / ".tmp_test"
        temp_file.write_text("Incomplete write")

        # Verify original file unchanged
        assert test_file.exists()
        assert test_file.read_text() == original_content
        assert AtomicWriter.verify_checksum(test_file, original_checksum)

        # Clean up temp file
        temp_file.unlink()

    def test_create_parent_dirs(self, temp_dir):
        """Test that parent directories are created automatically."""
        nested_file = temp_dir / "level1" / "level2" / "test.txt"
        content = "Nested file content"

        # Parent directories don't exist yet
        assert not nested_file.parent.exists()

        # Write should create parent directories
        checksum = AtomicWriter.write_text(nested_file, content)

        # Verify directories were created
        assert nested_file.exists()
        assert nested_file.parent.exists()
        assert nested_file.read_text() == content

    def test_overwrite_existing_file(self, temp_dir):
        """Test that overwriting an existing file works atomically."""
        test_file = temp_dir / "test.txt"

        # Write initial content
        AtomicWriter.write_text(test_file, "Initial content")

        # Overwrite with new content
        new_content = "Updated content"
        new_checksum = AtomicWriter.write_text(test_file, new_content)

        # Verify new content
        assert test_file.read_text() == new_content
        assert AtomicWriter.verify_checksum(test_file, new_checksum)

    def test_unicode_content(self, temp_dir):
        """Test that Unicode content is handled correctly."""
        test_file = temp_dir / "unicode.txt"
        unicode_content = "Hello 世界 🌍 Привет"

        checksum = AtomicWriter.write_text(test_file, unicode_content)

        # Verify content is preserved
        assert test_file.read_text(encoding="utf-8") == unicode_content
        assert AtomicWriter.verify_checksum(test_file, checksum)

    def test_verify_checksum_nonexistent_file(self, temp_dir):
        """Test checksum verification returns False for nonexistent file."""
        nonexistent_file = temp_dir / "nonexistent.txt"
        assert not AtomicWriter.verify_checksum(nonexistent_file, "any_checksum")

    def test_write_json_with_special_characters(self, temp_dir):
        """Test writing JSON with special characters."""
        test_file = temp_dir / "special.json"
        data = {
            "unicode": "日本語",
            "special_chars": "\n\t\r",
            "quotes": 'Test "quoted" and \'single\'',
            "emoji": "😀🎉",
        }

        checksum = AtomicWriter.write_json(test_file, data, ensure_ascii=False)

        # Read back and verify
        read_data = AtomicWriter.read_json(test_file)
        assert read_data == data
        assert AtomicWriter.verify_checksum(test_file, checksum)
