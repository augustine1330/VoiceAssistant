# command_parser.py
import re
from commands import browser, apps, system
from commands.ai_fallback import ask_ai

def parse_and_execute(transcript: str, tts, session):
    """
    Takes a raw transcript string.
    Tries to match it to a command.
    Executes the command or falls back to AI.
    Returns a spoken response string.
    """
    text = transcript.lower().strip()
    if not text:
        return None

    print(f"[Parser] Processing: '{text}'")

    # ─── SESSION CONTROL ──────────────────────────────────────────
    if any(p in text for p in ["stop listening", "go to sleep", "cancel", "goodbye", "shut up"]):
        session.end()
        return "Going to sleep. Say the wake word when you need me."

    # ─── BROWSER / TABS ───────────────────────────────────────────
    if re.search(r"open (a )?new tab|new tab", text):
        browser.new_tab()
        return "Opening a new tab."

    if re.search(r"close (this )?tab", text):
        browser.close_tab()
        return "Closing the tab."

    if re.search(r"go back|previous page", text):
        browser.go_back()
        return "Going back."

    if re.search(r"go forward|next page", text):
        browser.go_forward()
        return "Going forward."

    if re.search(r"refresh|reload (the page)?", text):
        browser.reload_page()
        return "Reloading the page."

    if re.search(r"incognito|private (window|tab)", text):
        browser.open_incognito()
        return "Opening incognito window."

    # ─── WEBSITES ─────────────────────────────────────────────────
    if re.search(r"open google|go to google", text):
        browser.open_google()
        return "Opening Google."

    if re.search(r"open youtube|go to youtube", text):
        browser.open_youtube()
        return "Opening YouTube."

    if re.search(r"open github|go to github", text):
        browser.open_github()
        return "Opening GitHub."

    if re.search(r"open gmail|check (my )?email|open email", text):
        browser.open_gmail()
        return "Opening Gmail."

    if re.search(r"open twitter|go to twitter", text):
        browser.open_twitter()
        return "Opening Twitter."

    if re.search(r"open linkedin|go to linkedin", text):
        browser.open_linkedin()
        return "Opening LinkedIn."

    if re.search(r"open whatsapp|go to whatsapp", text):
        browser.open_whatsapp()
        return "Opening WhatsApp."

    if re.search(r"open chat ?g ?p ?t|go to chatgpt", text):
        browser.open_chatgpt()
        return "Opening ChatGPT."

    if re.search(r"open claude|go to claude", text):
        browser.open_claude()
        return "Opening Claude."

    # Open a custom URL: "open amazon.com"
    url_match = re.search(r"open ([\w\-]+\.\w{2,})", text)
    if url_match:
        url = url_match.group(1)
        browser.open_url(url)
        return f"Opening {url}."

    # ─── SEARCH ───────────────────────────────────────────────────
    search_match = re.search(r"search (?:for |the web for |google for )?(.+)", text)
    if search_match:
        query = search_match.group(1).strip()
        browser.search_web(query)
        return f"Searching for {query}."

    yt_search_match = re.search(r"(?:search|find) (?:on |in )?youtube (?:for )?(.+)", text)
    if yt_search_match:
        query = yt_search_match.group(1).strip()
        browser.search_youtube(query)
        return f"Searching YouTube for {query}."

    maps_match = re.search(r"(?:navigate|directions?) to (.+)|open maps (?:for )?(.+)?", text)
    if maps_match:
        destination = (maps_match.group(1) or maps_match.group(2) or "").strip()
        browser.open_maps(destination)
        return f"Opening Maps{' for ' + destination if destination else ''}."

    # ─── APPLICATIONS ─────────────────────────────────────────────
    if re.search(r"open (vs ?code|visual studio code)", text):
        apps.open_vscode()
        return "Opening VS Code."

    if re.search(r"open terminal|open (command prompt|cmd|console)", text):
        apps.open_terminal()
        return "Opening terminal."

    if re.search(r"open (file manager|explorer|finder|files)", text):
        apps.open_file_manager()
        return "Opening file manager."

    if re.search(r"open calculator|open calc", text):
        apps.open_calculator()
        return "Opening calculator."

    if re.search(r"open notepad|open (text editor|notes)", text):
        apps.open_notepad()
        return "Opening notepad."

    if re.search(r"open (chrome|browser|internet)", text):
        apps.open_browser()
        return "Opening browser."

    if re.search(r"open spotify|play music", text):
        apps.open_spotify()
        return "Opening Spotify."

    if re.search(r"open slack", text):
        apps.open_slack()
        return "Opening Slack."

    if re.search(r"open discord", text):
        apps.open_discord()
        return "Opening Discord."

    if re.search(r"open zoom", text):
        apps.open_zoom()
        return "Opening Zoom."

    if re.search(r"open word|open microsoft word", text):
        apps.open_word()
        return "Opening Microsoft Word."

    if re.search(r"open excel|open spreadsheet", text):
        apps.open_excel()
        return "Opening Excel."

    if re.search(r"open powerpoint|open presentation", text):
        apps.open_powerpoint()
        return "Opening PowerPoint."

    if re.search(r"open task manager|check (cpu|memory|ram)", text):
        apps.open_task_manager()
        return "Opening Task Manager."

    if re.search(r"open settings|system settings|preferences", text):
        apps.open_settings()
        return "Opening settings."

    # ─── SCREEN CONTROL ───────────────────────────────────────────
    if re.search(r"scroll down", text):
        system.scroll_down()
        return "Scrolling down."

    if re.search(r"scroll up", text):
        system.scroll_up()
        return "Scrolling up."

    if re.search(r"scroll to (the )?(top|beginning)", text):
        system.scroll_to_top()
        return "Going to the top."

    if re.search(r"scroll to (the )?(bottom|end)", text):
        system.scroll_to_bottom()
        return "Going to the bottom."

    if re.search(r"take (a )?screenshot|capture (the )?screen", text):
        path = system.take_screenshot()
        return "Screenshot saved."

    if re.search(r"zoom in|make (it |this )?bigger", text):
        system.zoom_in()
        return "Zooming in."

    if re.search(r"zoom out|make (it |this )?smaller", text):
        system.zoom_out()
        return "Zooming out."

    if re.search(r"(reset|normal) zoom|zoom (reset|normal)", text):
        system.zoom_reset()
        return "Zoom reset."

    if re.search(r"find (on page|in page)|ctrl (f|find)", text):
        system.find_on_page()
        return "Opening find."

    if re.search(r"save (the )?(file|document|page)", text):
        system.save_file()
        return "Saving file."

    if re.search(r"select all", text):
        system.select_all()
        return "Selected all."

    if re.search(r"copy (that|this|it)?", text):
        system.copy()
        return "Copied."

    if re.search(r"paste (that|this|it)?", text):
        system.paste()
        return "Pasted."

    if re.search(r"undo (that)?", text):
        system.undo()
        return "Undone."

    if re.search(r"redo (that)?", text):
        system.redo()
        return "Redone."

    # ─── WINDOW MANAGEMENT ────────────────────────────────────────
    if re.search(r"minimize (the )?(window|this)?", text):
        system.minimize_window()
        return "Minimized."

    if re.search(r"maximize (the )?(window|this)?", text):
        system.maximize_window()
        return "Maximized."

    if re.search(r"close (the )?(window|this)", text):
        system.close_window()
        return "Closing window."

    if re.search(r"switch (to next |)(window|app)|alt tab", text):
        system.switch_window()
        return "Switching window."

    if re.search(r"show (the )?desktop", text):
        system.show_desktop()
        return "Showing desktop."

    # ─── TYPING ───────────────────────────────────────────────────
    type_match = re.search(r"type (.+)|write (.+)", text)
    if type_match:
        to_type = (type_match.group(1) or type_match.group(2)).strip()
        system.type_text(to_type)
        return f"Typed: {to_type}"

    if re.search(r"press enter|hit enter", text):
        system.press_enter()
        return "Enter pressed."

    if re.search(r"press escape|hit escape", text):
        system.press_escape()
        return "Escaped."

    # ─── VOLUME ───────────────────────────────────────────────────
    if re.search(r"volume up|increase volume|louder", text):
        system.increase_volume()
        return "Volume up."

    if re.search(r"volume down|decrease volume|quieter", text):
        system.decrease_volume()
        return "Volume down."

    if re.search(r"mute|silence", text):
        system.mute_volume()
        return "Muted."

    # ─── SYSTEM POWER ─────────────────────────────────────────────
    if re.search(r"lock (the )?(screen|computer|pc)", text):
        system.lock_screen()
        return "Locking screen."

    if re.search(r"shut ?down|power off", text):
        tts.speak("Shutting down in 5 seconds.")
        system.shutdown()
        return None

    if re.search(r"restart|reboot", text):
        tts.speak("Restarting in 5 seconds.")
        system.restart()
        return None

    # ─── AI FALLBACK ──────────────────────────────────────────────
    print("[Parser] No command matched — sending to local AI.")
    return ask_ai(transcript)