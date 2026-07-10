# commands/system.py
import pyautogui
import subprocess
import time
import os
from datetime import datetime
from config import OS

# Safety: disable pyautogui failsafe for smoother control
# (Move mouse to corner to emergency stop)
pyautogui.PAUSE = 0.1

def scroll_down(amount=500):
    pyautogui.scroll(-amount)

def scroll_up(amount=500):
    pyautogui.scroll(amount)

def scroll_to_top():
    pyautogui.hotkey("ctrl", "Home")

def scroll_to_bottom():
    pyautogui.hotkey("ctrl", "End")

def take_screenshot(save_dir="screenshots"):
    os.makedirs(save_dir, exist_ok=True)
    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(save_dir, filename)
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    print(f"[System] Screenshot saved: {filepath}")
    return filepath

def type_text(text: str):
    """Types text at the current cursor position."""
    pyautogui.write(text, interval=0.05)

def press_enter():
    pyautogui.press("enter")

def press_escape():
    pyautogui.press("escape")

def press_backspace(times=1):
    for _ in range(times):
        pyautogui.press("backspace")

def copy():
    pyautogui.hotkey("ctrl", "c")

def paste():
    pyautogui.hotkey("ctrl", "v")

def cut():
    pyautogui.hotkey("ctrl", "x")

def undo():
    pyautogui.hotkey("ctrl", "z")

def redo():
    pyautogui.hotkey("ctrl", "y")

def select_all():
    pyautogui.hotkey("ctrl", "a")

def save_file():
    pyautogui.hotkey("ctrl", "s")

def find_on_page():
    pyautogui.hotkey("ctrl", "f")

def zoom_in():
    pyautogui.hotkey("ctrl", "+")

def zoom_out():
    pyautogui.hotkey("ctrl", "-")

def zoom_reset():
    pyautogui.hotkey("ctrl", "0")

def minimize_window():
    pyautogui.hotkey("super", "down") if OS == "Windows" else pyautogui.hotkey("super", "h")

def maximize_window():
    pyautogui.hotkey("super", "up")

def close_window():
    pyautogui.hotkey("alt", "F4") if OS == "Windows" else pyautogui.hotkey("cmd", "q")

def switch_window():
    pyautogui.hotkey("alt", "tab")

def show_desktop():
    pyautogui.hotkey("super", "d")

def lock_screen():
    if OS == "Windows":
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
    elif OS == "Darwin":
        subprocess.run(["pmset", "displaysleepnow"])
    else:
        subprocess.run(["gnome-screensaver-command", "-l"])

def shutdown():
    if OS == "Windows":
        subprocess.run(["shutdown", "/s", "/t", "5"])
    elif OS == "Darwin":
        subprocess.run(["sudo", "shutdown", "-h", "now"])
    else:
        subprocess.run(["sudo", "shutdown", "-h", "now"])

def restart():
    if OS == "Windows":
        subprocess.run(["shutdown", "/r", "/t", "5"])
    elif OS == "Darwin":
        subprocess.run(["sudo", "shutdown", "-r", "now"])
    else:
        subprocess.run(["sudo", "reboot"])

def increase_volume():
    if OS == "Windows":
        pyautogui.press("volumeup")
    elif OS == "Darwin":
        subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])
    else:
        subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "10%+"])

def decrease_volume():
    if OS == "Windows":
        pyautogui.press("volumedown")
    elif OS == "Darwin":
        subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])
    else:
        subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "10%-"])

def mute_volume():
    pyautogui.press("volumemute")

def move_mouse(x: int, y: int):
    pyautogui.moveTo(x, y, duration=0.3)

def click(x=None, y=None):
    if x and y:
        pyautogui.click(x, y)
    else:
        pyautogui.click()

def right_click(x=None, y=None):
    if x and y:
        pyautogui.rightClick(x, y)
    else:
        pyautogui.rightClick()