# config.py
import os
import platform

# ─── Wake Word (openWakeWord) ──────────────────────────────────────
WAKE_WORD_NAME = None
WAKE_WORD_MODEL_PATH = "./models/custom/hey_amaghana.onnx"
WAKE_WORD_THRESHOLD = 0.6
WAKE_WORD_COOLDOWN = 1.0
WHISPER_MODEL_SIZE = "small.en"
NOISE_THRESHOLD = 10

# ─── Session ──────────────────────────────────────────────────────
SESSION_TIMEOUT_SECONDS = 30
COMMAND_SILENCE_TIMEOUT = 1

# ─── Audio ────────────────────────────────────────────────────────
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280

# ─── Ollama ───────────────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434/api/generate"
INTENT_MODEL = "phi3:mini"        # fast + reliable JSON for intent analysis
CONVERSATION_MODEL = "llama3"     # warmer responses for conversation
OLLAMA_MODEL = "llama3"           # kept for any legacy references

# ─── TTS ──────────────────────────────────────────────────────────
TTS_RATE = 175
TTS_VOLUME = 1.0

# ─── OS ───────────────────────────────────────────────────────────
OS = platform.system()            # "Windows", "Darwin", "Linux"

# ─── Vosk (kept as fallback reference, no longer primary) ─────────
VOSK_MODEL_PATH = os.path.join("models", "vosk-model-small-en-us-0.15")