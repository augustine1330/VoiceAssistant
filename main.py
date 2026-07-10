# main.py
import os
import time
import signal
import sys
import threading
import random

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from wake_word import WakeWordDetector
from listener import SpeechListener
from tts import TTS
from session import VoiceSession, SessionState
from conversation_manager import ConversationManager
from commands.ai_conversation import clear_history
from config import SESSION_TIMEOUT_SECONDS
from ui import VoiceUI

# ── Initialize UI ──────────────────────────────────────────────────
ui = VoiceUI()

# ── Initialize components ──────────────────────────────────────────
tts      = TTS()
listener = SpeechListener()

# ── Patch TTS to update UI when speaking ──────────────────────────
_original_speak = tts.speak

def _speak_with_ui(text: str):
    ui.show_tts(text)
    ui.set_state("responding")
    _original_speak(text)
    ui.set_state("listening")

tts.speak = _speak_with_ui

# ── Session callbacks ──────────────────────────────────────────────
def on_timeout():
    clear_history()
    ui.set_state("idle")
    _original_speak("I've gone quiet. Say Hey Jarvis to wake me up.")
    ui.show_tts("Say 'Hey Jarvis' to begin")

def on_state_change(state: SessionState):
    state_map = {
        SessionState.IDLE:       "idle",
        SessionState.LISTENING:  "listening",
        SessionState.PROCESSING: "processing",
        SessionState.EXECUTING:  "executing",
        SessionState.SLEEPING:   "idle",
    }
    ui.set_state(state_map.get(state, "idle"))

session = VoiceSession(
    timeout=SESSION_TIMEOUT_SECONDS,
    on_timeout=on_timeout,
    on_state_change=on_state_change,
)

manager = ConversationManager(tts, listener, session)

# ── Wake word handler ──────────────────────────────────────────────
def on_wake_word():
    if session.state != SessionState.IDLE:
        return

    greetings =[
            "Yes Augustine?",
            "I'm listening.",
            "Hey! What do you need?",
            "Go ahead Augustine.",
            "How can I help?",
            "What's up?",
            "Ready when you are.",
        ]

    greeting = random.choice(greetings)
    ui.set_state("listening")
    ui.show_tts(greeting)
    _original_speak(greeting)
    session.start()

    # Run command loop in background so UI stays responsive
    t = threading.Thread(target=command_loop, daemon=True)
    t.start()

# ── Command loop ───────────────────────────────────────────────────
def command_loop():
    while session.state != SessionState.IDLE:
        session.set_listening()
        ui.set_state("listening")
        ui.clear_stt()

        transcript = listener.listen_for_command()

        if not transcript:
            print("[Main] No speech detected, waiting...")
            time.sleep(0.5)
            continue

        ui.show_stt(transcript)
        session.reset_timer()

        ui.set_state("processing")
        manager.process(transcript)

        time.sleep(0.2)

    ui.set_state("idle")
    print("[Main] Session ended.")

# ── Graceful shutdown ──────────────────────────────────────────────
def handle_exit(sig, frame):
    print("\n[Main] Shutting down...")
    try:
        wake_detector.cleanup()
    except:
        pass
    print("[Main] Goodbye.")
    os._exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

# ── Start ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  Kofi Jarvis Voice Assistant")
    print("  Say 'Hey Jarvis' to begin")
    print("  Ctrl+C to exit")
    print("=" * 50)

    # Start wake detector in background
    wake_detector = WakeWordDetector(on_detected=on_wake_word)
    wake_detector.start()

    # Speak intro in background thread
    def intro():
        time.sleep(1)
        _original_speak("Am Kofi Jarvis. Say Hey Jarvis to get started.")

    threading.Thread(target=intro, daemon=True).start()

    # UI must run on main thread — this blocks until window closes
    ui.run()