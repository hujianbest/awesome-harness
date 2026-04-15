"""State machine for managing workflow session state transitions."""

import logging
import threading
from datetime import datetime
from typing import Callable, Optional

from garage_os.types import SessionState, StateTransition

logger = logging.getLogger(__name__)


class InvalidStateTransitionError(Exception):
    """Exception raised when an invalid state transition is attempted."""

    def __init__(self, from_state: SessionState, to_state: SessionState):
        self.from_state = from_state
        self.to_state = to_state
        super().__init__(f"Invalid transition: {from_state.value} -> {to_state.value}")


class StateMachine:
    """Execution state machine for managing SessionState transitions."""

    # Valid transition table
    VALID_TRANSITIONS: dict[SessionState, set[SessionState]] = {
        SessionState.IDLE: {SessionState.RUNNING, SessionState.ARCHIVED},
        SessionState.RUNNING: {
            SessionState.PAUSED,
            SessionState.COMPLETED,
            SessionState.FAILED,
            SessionState.ARCHIVED,
        },
        SessionState.PAUSED: {SessionState.RUNNING, SessionState.ARCHIVED},
        SessionState.FAILED: {SessionState.RUNNING, SessionState.ARCHIVED},  # retry
        SessionState.COMPLETED: {SessionState.ARCHIVED},
        SessionState.ARCHIVED: set(),  # terminal
    }

    def __init__(self, initial_state: SessionState = SessionState.IDLE):
        """Initialize the state machine with an initial state."""
        self._current_state = initial_state
        self._history: list[StateTransition] = []
        self._lock = threading.Lock()
        self._transition_callbacks: list[Callable[[StateTransition], None]] = []
        self._enter_callbacks: dict[SessionState, list[Callable[[StateTransition], None]]] = {
            state: [] for state in SessionState
        }

    def transition(
        self,
        to_state: SessionState,
        reason: str = "",
        metadata: Optional[dict] = None,
    ) -> StateTransition:
        """Execute a state transition.

        Args:
            to_state: The target state to transition to.
            reason: Optional reason for the transition.
            metadata: Optional metadata dict for the transition.

        Returns:
            The StateTransition record that was created.

        Raises:
            InvalidStateTransitionError: If the transition is not valid.
        """
        with self._lock:
            if not self.can_transition(to_state):
                raise InvalidStateTransitionError(self._current_state, to_state)

            from_state = self._current_state
            transition_record = StateTransition(
                from_state=from_state,
                to_state=to_state,
                timestamp=datetime.now(),
                reason=reason,
                metadata=metadata or {},
            )

            self._history.append(transition_record)
            self._current_state = to_state

        # Fire callbacks after releasing the lock to avoid potential deadlocks
        self._fire_callbacks(transition_record)

        return transition_record

    def can_transition(self, to_state: SessionState) -> bool:
        """Check if a transition to the target state is valid.

        Args:
            to_state: The target state to check.

        Returns:
            True if the transition is valid, False otherwise.
        """
        return to_state in self.VALID_TRANSITIONS[self._current_state]

    def get_valid_transitions(self) -> set[SessionState]:
        """Get all valid target states from the current state.

        Returns:
            A set of SessionState values that are valid targets.
        """
        return self.VALID_TRANSITIONS[self._current_state].copy()

    @property
    def current_state(self) -> SessionState:
        """Get the current state."""
        return self._current_state

    @property
    def history(self) -> list[StateTransition]:
        """Get a copy of the transition history."""
        return list(self._history)

    def on_transition(self, callback: Callable[[StateTransition], None]) -> None:
        """Register a callback to be invoked on any state transition.

        Args:
            callback: A function that takes a StateTransition object.
        """
        with self._lock:
            self._transition_callbacks.append(callback)

    def on_enter(
        self,
        state: SessionState,
        callback: Callable[[StateTransition], None],
    ) -> None:
        """Register a callback to be invoked when entering a specific state.

        Args:
            state: The state to watch for entry.
            callback: A function that takes a StateTransition object.
        """
        with self._lock:
            self._enter_callbacks[state].append(callback)

    def _fire_callbacks(self, transition: StateTransition) -> None:
        """Fire all applicable callbacks for a transition.

        Callback exceptions are caught and logged to prevent breaking
        the state transition.

        Args:
            transition: The transition that just occurred.
        """
        # Fire on_transition callbacks
        for callback in self._transition_callbacks:
            try:
                callback(transition)
            except Exception as e:
                logger.warning(
                    f"on_transition callback failed: {e}",
                    exc_info=True,
                )

        # Fire on_enter callbacks for the target state
        for callback in self._enter_callbacks[transition.to_state]:
            try:
                callback(transition)
            except Exception as e:
                logger.warning(
                    f"on_enter callback failed for state {transition.to_state.value}: {e}",
                    exc_info=True,
                )

    def reset(self, state: SessionState = SessionState.IDLE) -> None:
        """Reset the state machine to a given state and clear history.

        Args:
            state: The state to reset to. Defaults to IDLE.
        """
        with self._lock:
            self._current_state = state
            self._history.clear()
