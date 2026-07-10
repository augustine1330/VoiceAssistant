# commands/apps.py
import subprocess
from config import OS

def _run(windows_cmd=None, mac_cmd=None, linux_cmd=None):
    """Cross-platform app launcher."""
    try:
        if OS == "Windows" and windows_cmd:
            subprocess.Popen(windows_cmd, shell=True)
        elif OS == "Darwin" and mac_cmd:
            subprocess.Popen(mac_cmd, shell=True)
        elif OS == "Linux" and linux_cmd:
            subprocess.Popen(linux_cmd, shell=True)
        return True
    except Exception as e:
        print(f"[Apps] Error launching app: {e}")
        return False

def open_vscode():
    return _run("code", "code", "code")

def open_terminal():
    return _run(
        windows_cmd="start cmd",
        mac_cmd="open -a Terminal",
        linux_cmd="x-terminal-emulator"
    )

def open_file_manager():
    return _run(
        windows_cmd="explorer",
        mac_cmd="open .",
        linux_cmd="nautilus"
    )

def open_calculator():
    return _run(
        windows_cmd="calc",
        mac_cmd="open -a Calculator",
        linux_cmd="gnome-calculator"
    )

def open_notepad():
    return _run(
        windows_cmd="notepad",
        mac_cmd="open -a TextEdit",
        linux_cmd="gedit"
    )

def open_browser():
    return _run(
        windows_cmd="start chrome",
        mac_cmd="open -a 'Google Chrome'",
        linux_cmd="google-chrome"
    )

def open_spotify():
    return _run(
        windows_cmd="start spotify",
        mac_cmd="open -a Spotify",
        linux_cmd="spotify"
    )

def open_slack():
    return _run(
        windows_cmd="start slack",
        mac_cmd="open -a Slack",
        linux_cmd="slack"
    )

def open_discord():
    return _run(
        windows_cmd="start discord",
        mac_cmd="open -a Discord",
        linux_cmd="discord"
    )

def open_zoom():
    return _run(
        windows_cmd="start zoom",
        mac_cmd="open -a zoom.us",
        linux_cmd="zoom"
    )

def open_word():
    return _run(
        windows_cmd="start winword",
        mac_cmd="open -a 'Microsoft Word'",
        linux_cmd="libreoffice --writer"
    )

def open_excel():
    return _run(
        windows_cmd="start excel",
        mac_cmd="open -a 'Microsoft Excel'",
        linux_cmd="libreoffice --calc"
    )

def open_powerpoint():
    return _run(
        windows_cmd="start powerpnt",
        mac_cmd="open -a 'Microsoft PowerPoint'",
        linux_cmd="libreoffice --impress"
    )

def open_task_manager():
    return _run(
        windows_cmd="taskmgr",
        mac_cmd="open -a 'Activity Monitor'",
        linux_cmd="gnome-system-monitor"
    )

def open_settings():
    return _run(
        windows_cmd="start ms-settings:",
        mac_cmd="open -a 'System Preferences'",
        linux_cmd="gnome-control-center"
    )

def open_file(filepath: str):
    """Open any specific file."""
    return _run(
        windows_cmd=f'start "" "{filepath}"',
        mac_cmd=f'open "{filepath}"',
        linux_cmd=f'xdg-open "{filepath}"'
    )