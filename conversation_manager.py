# conversation_manager.py
import time
from commands.intent_analyzer import analyze_intent
from commands.ai_conversation import chat, chat_about_failed_command, clear_history
from command_executor import execute

YES_WORDS = [
    "yes", "yeah", "yep", "sure", "okay", "ok",
    "do it", "go ahead", "correct", "right",
    "please", "yea", "yup", "absolutely"
]

NO_WORDS = [
    "no", "nope", "nah", "dont", "stop", "cancel",
    "negative", "not that", "wrong", "never mind", "nevermind"
]

class ConversationManager:
    def __init__(self, tts, listener, session):
        self.tts = tts
        self.listener = listener
        self.session = session
        self._pending_command_id = None
        self._pending_params = {}
        self._pending_suggestion = ""

    def process(self, transcript: str):
        if not transcript.strip():
            return

        text = transcript.lower().strip()

        if self._pending_command_id:
            self._handle_confirmation(text)
            return

        self.session.set_processing()
        intent = analyze_intent(transcript)

        intent_type = intent.get("type", "conversation")
        command_id = intent.get("command_id")
        params = intent.get("params", {})

        if intent_type == "exact" and command_id:
            self._execute_command(command_id, params)
        elif intent_type == "suggest" and command_id:
            suggestion_text = intent.get(
                "suggestion_text",
                f"Did you mean {command_id.replace(chr(95), chr(32))}?"
            )
            self._make_suggestion(command_id, params, suggestion_text)
        else:
            self._converse(transcript)

    def _execute_command(self, command_id: str, params: dict):
        self.session.set_executing()

        if command_id in ["shutdown", "restart"]:
            action = "shut down" if command_id == "shutdown" else "restart"
            self._make_suggestion(
                command_id, params,
                f"Just to confirm, you want me to {action} the computer?"
            )
            return

        result = execute(command_id, params)

        if result == "__END_SESSION__":
            self.tts.speak("Going to sleep. Say Hey Amaghana when you need me.")
            clear_history()
            self.session.end()
            return

        elif result == "__SHUTDOWN__":
            self.tts.speak("Shutting down in 5 seconds. Goodbye.")
            time.sleep(1)
            from commands.system import shutdown
            shutdown()
            return

        elif result == "__RESTART__":
            self.tts.speak("Restarting in 5 seconds.")
            time.sleep(1)
            from commands.system import restart
            restart()
            return

        elif result:
            self.tts.speak(result)
        else:
            response = chat_about_failed_command(command_id)
            self.tts.speak(response)

        self.session.set_listening()
        self.session.reset_timer()

    def _make_suggestion(self, command_id: str, params: dict, suggestion_text: str):
        self._pending_command_id = command_id
        self._pending_params = params
        self._pending_suggestion = suggestion_text
        self.tts.speak(suggestion_text)
        self.session.set_listening()
        self.session.reset_timer()

    def _handle_confirmation(self, text: str):
        if any(word in text for word in YES_WORDS):
            self.tts.speak("Got it.")
            command_id = self._pending_command_id
            params = self._pending_params
            self._clear_pending()
            self._execute_command(command_id, params)
        elif any(word in text for word in NO_WORDS):
            self._clear_pending()
            self.tts.speak("No problem. What would you like to do instead?")
            self.session.set_listening()
            self.session.reset_timer()
        else:
            self.tts.speak(f"Sorry, I did not catch that. {self._pending_suggestion}")
            self.session.set_listening()
            self.session.reset_timer()

    def _converse(self, transcript: str):
        self.session.set_executing()
        try:
            response = chat(transcript)
            self.tts.speak(response)
        except Exception as e:
            print(f"[Manager] Conversation error: {e}")
            self.tts.speak("Sorry, I lost my train of thought there. What were you saying?")
        self.session.set_listening()
        self.session.reset_timer()

    def _clear_pending(self):
        self._pending_command_id = None
        self._pending_params = {}
        self._pending_suggestion = ""
