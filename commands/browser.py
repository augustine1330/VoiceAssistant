# commands/browser.py
import webbrowser
import subprocess
from config import OS

def open_new_tab(url="about:blank"):
    webbrowser.open_new_tab(url)

def open_google():
    webbrowser.open_new_tab("https://www.google.com")

def open_youtube():
    webbrowser.open_new_tab("https://www.youtube.com")

def open_github():
    webbrowser.open_new_tab("https://github.com")

def open_gmail():
    webbrowser.open_new_tab("https://mail.google.com")

def open_twitter():
    webbrowser.open_new_tab("https://twitter.com")

def open_linkedin():
    webbrowser.open_new_tab("https://www.linkedin.com")

def open_whatsapp():
    webbrowser.open_new_tab("https://web.whatsapp.com")

def open_chatgpt():
    webbrowser.open_new_tab("https://chat.openai.com")

def open_claude():
    webbrowser.open_new_tab("https://claude.ai")

def search_web(query: str):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open_new_tab(url)

def search_youtube(query: str):
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open_new_tab(url)

def open_maps(destination: str = ""):
    if destination:
        url = f"https://maps.google.com/?q={destination.replace(' ', '+')}"
    else:
        url = "https://maps.google.com"
    webbrowser.open_new_tab(url)

def open_url(url: str):
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open_new_tab(url)

def go_back():
    import pyautogui
    import time
    pyautogui.hotkey("alt", "left")

def go_forward():
    import pyautogui
    pyautogui.hotkey("alt", "right")

def reload_page():
    import pyautogui
    pyautogui.hotkey("ctrl", "r")

def close_tab():
    import pyautogui
    pyautogui.hotkey("ctrl", "w")

def new_tab():
    import pyautogui
    pyautogui.hotkey("ctrl", "t")

def open_incognito():
    import pyautogui
    pyautogui.hotkey("ctrl", "shift", "n")