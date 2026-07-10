# session.py
import threading
import time
from enum import Enum

class SessionState(Enum):
    IDLE       = "idle"
    LISTENING  = "listening"
    PROCESSING = "processing"
    EXECUTING  = "executing"
    SLEEPING   = "sleeping"

class VoiceSession:
    def __init__(self, timeout: int, on_timeout, on_state_change=None):
        self.timeout = timeout
        self.on_timeout = on_timeout
        self.on_state_change = on_state_change
        self.state = SessionState.IDLE
        self._timer = None
        self._start_time = None

    def start(self):
        """Called when wake word is detected."""
        self._set_state(SessionState.LISTENING)
        self._start_time = time.time()
        self._reset_timer()

    def reset_timer(self):
        """Call this every time the user speaks — restarts the 30s window."""
        if self.state != SessionState.IDLE:
            self._reset_timer()

    def time_remaining(self) -> float:
        if self._start_time is None:
            return 0
        elapsed = time.time() - self._start_time
        return max(0, self.timeout - elapsed)

    def set_processing(self):
        self._set_state(SessionState.PROCESSING)

    def set_executing(self):
        self._set_state(SessionState.EXECUTING)

    def set_listening(self):
        self._set_state(SessionState.LISTENING)
        self._reset_timer()

    def end(self):
        self._cancel_timer()
        self._set_state(SessionState.IDLE)

    def _reset_timer(self):
        self._cancel_timer()
        self._start_time = time.time()
        self._timer = threading.Timer(self.timeout, self._timeout_handler)
        self._timer.daemon = True
        self._timer.start()

    def _cancel_timer(self):
        if self._timer:
            self._timer.cancel()
            self._timer = None

    def _timeout_handler(self):
        print("[Session] 30 seconds elapsed — going to sleep.")
        self._set_state(SessionState.IDLE)
        self.on_timeout()

    def _set_state(self, state: SessionState):
        self.state = state
        print(f"[Session] State → {state.value}")
        if self.on_state_change:
            self.on_state_change(state)