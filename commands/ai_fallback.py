# commands/ai_conversation.py
import requests
from config import OLLAMA_URL, OLLAMA_MODEL

SYSTEM_PROMPT = """You are Amaghana, a friendly and intelligent voice assistant running 
locally on the user's computer. You have a warm, helpful personality.

Rules for responses:
- Keep responses SHORT — maximum 2-3 sentences when possible
- Speak naturally as if talking out loud — no markdown, no bullet points, no lists
- Be warm, friendly and conversational
- If you don't know something, say so honestly
- For factual questions, answer directly and concisely
- Never mention that you are an AI unless directly asked
- Never say "As an AI language model..."
- You can do small talk, answer questions, tell jokes, and help think through problems
- Always end with something that invites the user to continue if relevant

Examples of good responses:
User: "What is machine learning?"
You: "Machine learning is how computers learn from data instead of being explicitly programmed. Think of it like teaching a child by showing examples rather than giving strict rules. Want me to go deeper on any part of that?"

User: "Tell me a joke"  
You: "Why do programmers prefer dark mode? Because light attracts bugs! Hope that one landed."

User: "What time is it?"
You: "I don't have access to your system clock right now, but you can check the bottom right corner of your screen."
"""

# Conversation history — keeps context across turns in a session
_conversation_history = []

def chat(user_message: str) -> str:
    """Send message to Ollama with full conversation history for context."""
    global _conversation_history

    # Add user message to history
    _conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # Build prompt with history
    history_text = ""
    for turn in _conversation_history[-6:]:  # keep last 6 turns for context
        role = "User" if turn["role"] == "user" else "Amaghana"
        history_text += f"{role}: {turn['content']}\n"

    full_prompt = f"{SYSTEM_PROMPT}\n\nConversation:\n{history_text}Amaghana:"

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.75,
                    "num_predict": 120,
                }
            },
            timeout=30
        )

        reply = response.json().get("response", "").strip()
        # Clean any accidental markdown
        reply = reply.replace("*", "").replace("#", "").replace("`", "")

        # Add assistant reply to history
        _conversation_history.append({
            "role": "assistant",
            "content": reply
        })

        return reply if reply else "I didn't catch that. Could you say that again?"

    except requests.exceptions.ConnectionError:
        return "The local AI isn't responding. Make sure Ollama is running."
    except Exception as e:
        print(f"[AI] Error: {e}")
        return "Something went wrong on my end. Try again?"

def clear_history():
    """Call this when session ends to reset conversation context."""
    global _conversation_history
    _conversation_history = []
    print("[AI] Conversation history cleared.")