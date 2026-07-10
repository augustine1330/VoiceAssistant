# commands/intent_analyzer.py
import re
import json
import requests
from config import OLLAMA_URL, INTENT_MODEL

# Full command list the AI chooses from
COMMANDS_LIST = """
BROWSER: new_tab, close_tab, go_back, go_forward, reload_page, incognito
WEBSITES: open_google, open_youtube, open_github, open_gmail, open_whatsapp,
          open_twitter, open_maps, open_chatgpt, open_claude, open_linkedin,
          open_browser, open_spotify
APPS: open_vscode, open_terminal, open_calculator, open_notepad, open_discord,
      open_zoom, open_word, open_excel, open_settings, task_manager, open_files
SCREEN: scroll_down, scroll_up, scroll_top, scroll_bottom, screenshot,
        zoom_in, zoom_out, zoom_reset, find
EDIT: copy, paste, undo, redo, select_all, save_file, type_text
WINDOW: minimize, maximize, close_window, switch_window, show_desktop
SYSTEM: volume_up, volume_down, mute, lock_screen, shutdown, restart
SEARCH: search_web (needs query), search_youtube (needs query),
        open_url (needs url), open_maps_dest (needs destination),
        type_text (needs text)
SESSION: end_session
"""

PROMPT = '''You are an AI command parser for a voice assistant.
The user said: "{transcript}"

Available commands:
{commands}

Rules:
- Understand natural language, not just exact phrases
- "close chrome", "shut chrome", "exit browser" all mean close_window
- "look up", "google", "find me" all mean search_web
- "put on music", "play spotify" means open_spotify
- "go to youtube", "open videos" means open_youtube
- "type hello", "write hello" means type_text with text=hello
- "get directions to X", "take me to X" means open_maps_dest
- Anything that sounds like a question or chat = conversation

Return ONLY valid JSON, nothing else:

If it is a command:
{{"type":"exact","command_id":"open_youtube","params":{{}},"confidence":0.95}}

If it needs a parameter:
{{"type":"exact","command_id":"search_web","params":{{"query":"python tutorials"}},"confidence":0.95}}
{{"type":"exact","command_id":"type_text","params":{{"text":"hello world"}},"confidence":0.95}}
{{"type":"exact","command_id":"open_maps_dest","params":{{"destination":"accra mall"}},"confidence":0.95}}
{{"type":"exact","command_id":"open_url","params":{{"url":"amazon.com"}},"confidence":0.95}}

If it is conversation:
{{"type":"conversation","command_id":null,"params":{{}},"confidence":0.0}}

User said: "{transcript}"
JSON:'''


def _clean(transcript: str) -> str:
    """Remove STT repetitions."""
    text = transcript.strip()

    # Take first sentence only
    if "." in text:
        text = text.split(".")[0].strip()

    # Remove repeated phrases
    words = text.split()
    half  = len(words) // 2
    if half > 2 and words[:half] == words[half:]:
        text = " ".join(words[:half])
        print(f"[Intent] Cleaned repetition → '{text}'")

    return text.strip()


def analyze_intent(transcript: str) -> dict:
    """
    Send everything to Ollama — no hardcoded patterns.
    Pure AI understanding of what the user meant.
    """
    text = _clean(transcript)
    print(f"[Intent] Analyzing: '{text}'")

    prompt = PROMPT.format(
        transcript=text,
        commands=COMMANDS_LIST
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": INTENT_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.0,
                    "num_predict": 60,
                    "num_thread": 8,
                    "num_ctx": 1024,
                    "stop": ["\n\n", "User said", "Rules"],
                }
            },
            timeout=45
        )

        raw = response.json().get("response", "").strip()

        # Clean markdown if model adds it
        raw = raw.replace("```json", "").replace("```", "").strip()

        # Extract JSON object
        match = re.search(r'\{.*?\}', raw, re.DOTALL)
        if match:
            raw = match.group(0)

        result = json.loads(raw)

        print(f"[Intent] → type={result.get('type')} "
              f"cmd={result.get('command_id')} "
              f"params={result.get('params')} "
              f"confidence={result.get('confidence', 0):.2f}")

        return result

    except json.JSONDecodeError:
        print(f"[Intent] JSON parse failed — treating as conversation")
        return _conversation()

    except requests.exceptions.Timeout:
        print(f"[Intent] Ollama timeout — treating as conversation")
        return _conversation()

    except Exception as e:
        print(f"[Intent] Error: {e}")
        return _conversation()


def _conversation():
    return {
        "type": "conversation",
        "command_id": None,
        "params": {},
        "confidence": 0.0
    }