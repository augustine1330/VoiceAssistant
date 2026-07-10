# test_stt.py
from listener import SpeechListener
listener = SpeechListener()
print("\nSay something now...")
result = listener.listen_for_command()
if result:
    print(f"\n✅ Transcript: '{result}'")
else:
    print("\n❌ Nothing heard — check mic or lower NOISE_THRESHOLD in config.py") 