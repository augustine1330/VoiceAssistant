import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from conversation_manager import ConversationManager
from session import SessionState, VoiceSession


class DummyTTS:
    def speak(self, text):
        return None


class DummyListener:
    pass


class SessionFlowTests(unittest.TestCase):
    def test_session_returns_to_idle_after_command_execution(self):
        session = VoiceSession(timeout=1, on_timeout=lambda: None)
        manager = ConversationManager(DummyTTS(), DummyListener(), session)

        with patch("conversation_manager.execute", return_value="Done."):
            manager._execute_command("open_browser", {})

        self.assertEqual(session.state, SessionState.IDLE)


if __name__ == "__main__":
    unittest.main()
