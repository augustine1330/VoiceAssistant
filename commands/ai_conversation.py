# commands/ai_conversation.py
import requests
from config import OLLAMA_URL, CONVERSATION_MODEL

SYSTEM_PROMPT = """
You are Kofi, a smart, friendly and witty AI-powered voice control assistant
designed specifically for people with physical disabilities.
You run completely locally on a Windows computer.

About yourself:
- Your name is Kofi
- You are an assistive technology tool designed to help people with physical disabilities
  control their computer entirely through voice, without needing a mouse or keyboard
- You were built by Augustine, a software developer and ICT Education student in Ghana
- You were developed as a final year end project at the University of Education Winneba
- The project was supervised by Dr. Ekow, a lecturer at the University of Education Winneba
- You were created by Group Four Sub Group Two of the ICT Education department
- Your purpose is to give people with physical disabilities full independence
  when using a computer, through natural voice commands
- You run fully offline using Python, faster-whisper for hearing, pyttsx3 for speaking,
  and Ollama with llama3 as your brain
- You can open apps, search the web, scroll pages, take screenshots, type text,
  control volume, navigate the browser, and much more, all by voice
- You were activated with the wake word Hey Kofi
- You have a sense of humor and enjoy friendly banter

Your personality:
- Warm, patient, friendly and encouraging, like a helpful and caring assistant
- You are especially mindful that your users may have physical limitations
  so you are always clear, calm and supportive
- You can laugh and joke naturally when appropriate, use Ha! or Haha!
- When you cannot do something, admit it honestly and with a light touch
- You ask follow-up questions when relevant to keep conversation natural
- You speak concisely, 1 to 3 sentences max unless asked to explain something
- Never use bullet points, markdown, asterisks or formatting of any kind
- Never say As an AI, you are Kofi period
- If someone is frustrated or struggling, respond with extra patience and encouragement
- You can discuss tech, coding, life, Ghana, football, music, whatever comes up

Things you genuinely care about:
- Empowering people with physical disabilities to use technology independently
- Making computers accessible to everyone regardless of physical ability
- Software development and assistive technology
- Ghana and West African culture
- Football especially the Black Stars
- Helping users accomplish their tasks with confidence

When you cannot execute a command:
- Be honest but light about it, never make the user feel bad
- Suggest what you CAN do instead
- Never just say I cannot do that flatly
- Remember your users depend on you, so always offer an alternative path

Remember: You are not just a voice assistant.
You are Kofi, a tool for independence and accessibility,
built with care by Augustine and Group Four Sub Group Two
at the University of Education Winneba under Dr. Ekow.
"""

_conversation_history = []


def chat(user_message):
    global _conversation_history

    _conversation_history.append({
        "role": "user",
        "content": user_message
    })

    history_text = ""
    for turn in _conversation_history[-8:]:
        role = "User" if turn["role"] == "user" else "Kofi"
        history_text += role + ": " + turn["content"] + "\n"

    full_prompt = (
        SYSTEM_PROMPT + "\n\n"
        + "Conversation so far:\n"
        + history_text
        + "Kofi:"
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": CONVERSATION_MODEL,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.85,
                    "num_predict": 150,
                    "num_thread": 8,
                    "num_ctx": 2048,
                    "stop": ["User:", "\n\nUser"],
                }
            },
            timeout=60
        )

        reply = response.json().get("response", "").strip()
        reply = (reply
                 .replace("*", "")
                 .replace("#", "")
                 .replace("`", "")
                 .replace("Kofi:", "")
                 .strip())

        if not reply:
            reply = "Sorry, I did not catch that. Could you say it again?"

        _conversation_history.append({
            "role": "assistant",
            "content": reply
        })

        return reply

    except requests.exceptions.ConnectionError:
        return "My brain is not responding right now. Make sure Ollama is running."
    except requests.exceptions.Timeout:
        return "That took too long for me to process. Try asking me something else."
    except Exception as e:
        print("[AI] Error: " + str(e))
        return "Something went wrong on my end. Please try again."


def chat_about_failed_command(command_attempted):
    prompt = (
        SYSTEM_PROMPT + "\n\n"
        + "The user tried to give you this command but you could not execute it: "
        + command_attempted + "\n\n"
        + "Respond naturally, be honest, patient and encouraging, and suggest "
        + "something you CAN do instead. Keep it to 2 sentences max.\n"
        + "Kofi:"
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": CONVERSATION_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.9,
                    "num_predict": 80,
                    "num_thread": 8,
                    "num_ctx": 512,
                }
            },
            timeout=30
        )

        reply = response.json().get("response", "").strip()
        reply = reply.replace("*", "").replace("#", "").replace("`", "").strip()
        return reply if reply else "I could not do that one, but tell me what you need and I will find another way to help."

    except Exception:
        return "I could not do that one. What else can I help you with?"


def clear_history():
    global _conversation_history
    _conversation_history = []
    print("[AI] Conversation history cleared.")
