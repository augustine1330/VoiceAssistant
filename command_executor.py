# command_executor.py
from commands import browser, apps, system

def execute(command_id: str, params: dict = {}) -> str:
    """
    Takes a command_id and optional params dict.
    Executes the action and returns a friendly voice response.
    """

    # ── BROWSER ──────────────────────────────────────────────────
    if command_id == "new_tab":
        browser.new_tab()
        return "Opening a new tab for you."

    if command_id == "close_tab":
        browser.close_tab()
        return "Tab closed."

    if command_id == "go_back":
        browser.go_back()
        return "Going back."

    if command_id == "go_forward":
        browser.go_forward()
        return "Going forward."

    if command_id == "reload_page":
        browser.reload_page()
        return "Page reloaded."

    if command_id == "incognito":
        browser.open_incognito()
        return "Opening a private window."

    # ── WEBSITES ─────────────────────────────────────────────────
    if command_id == "open_google":
        browser.open_google()
        return "Here's Google."

    if command_id == "open_youtube":
        browser.open_youtube()
        return "Opening YouTube for you."

    if command_id == "open_github":
        browser.open_github()
        return "GitHub is open."

    if command_id == "open_gmail":
        browser.open_gmail()
        return "Let me pull up your Gmail."

    if command_id == "open_whatsapp":
        browser.open_whatsapp()
        return "Opening WhatsApp Web."

    if command_id == "open_twitter":
        browser.open_twitter()
        return "Opening Twitter."

    if command_id == "open_maps":
        browser.open_maps()
        return "Opening Google Maps."

    if command_id == "open_chatgpt":
        browser.open_chatgpt()
        return "Opening ChatGPT."

    if command_id == "open_claude":
        browser.open_claude()
        return "Opening Claude."

    # ── SEARCH ───────────────────────────────────────────────────
    if command_id == "search_web":
        query = params.get("query", "")
        if query:
            browser.search_web(query)
            return f"Searching Google for {query}."
        return "What would you like me to search for?"

    if command_id == "search_youtube":
        query = params.get("query", "")
        if query:
            browser.search_youtube(query)
            return f"Searching YouTube for {query}."
        return "What should I search on YouTube?"

    if command_id == "open_url":
        url = params.get("url", "")
        if url:
            browser.open_url(url)
            return f"Opening {url}."
        return "Which website would you like me to open?"

    if command_id == "open_maps_dest":
        destination = params.get("destination", "")
        if destination:
            browser.open_maps(destination)
            return f"Getting directions to {destination}."
        return "Where would you like to navigate to?"

    # ── APPS ─────────────────────────────────────────────────────
    if command_id == "open_vscode":
        apps.open_vscode()
        return "VS Code is launching."

    if command_id == "open_terminal":
        apps.open_terminal()
        return "Terminal is open."

    if command_id == "open_files":
        apps.open_file_manager()
        return "Opening your file manager."

    if command_id == "open_calculator":
        apps.open_calculator()
        return "Calculator is open."

    if command_id == "open_notepad":
        apps.open_notepad()
        return "Opening notepad."

    if command_id == "open_browser":
        apps.open_browser()
        return "Opening your browser."

    if command_id == "open_spotify":
        apps.open_spotify()
        return "Opening Spotify. Enjoy the music."

    if command_id == "open_discord":
        apps.open_discord()
        return "Discord is opening."

    if command_id == "open_zoom":
        apps.open_zoom()
        return "Opening Zoom."

    if command_id == "open_word":
        apps.open_word()
        return "Microsoft Word is launching."

    if command_id == "open_excel":
        apps.open_excel()
        return "Opening Excel."

    if command_id == "open_settings":
        apps.open_settings()
        return "Opening system settings."

    if command_id == "task_manager":
        apps.open_task_manager()
        return "Opening Task Manager."

    # ── SCREEN ───────────────────────────────────────────────────
    if command_id == "scroll_down":
        system.scroll_down()
        return "Scrolling down."

    if command_id == "scroll_up":
        system.scroll_up()
        return "Scrolling up."

    if command_id == "scroll_top":
        system.scroll_to_top()
        return "Going to the top."

    if command_id == "scroll_bottom":
        system.scroll_to_bottom()
        return "Jumping to the bottom."

    if command_id == "screenshot":
        path = system.take_screenshot()
        return "Screenshot taken and saved."

    if command_id == "zoom_in":
        system.zoom_in()
        return "Zoomed in."

    if command_id == "zoom_out":
        system.zoom_out()
        return "Zoomed out."

    if command_id == "zoom_reset":
        system.zoom_reset()
        return "Zoom back to normal."

    # ── EDITING ──────────────────────────────────────────────────
    if command_id == "copy":
        system.copy()
        return "Copied."

    if command_id == "paste":
        system.paste()
        return "Pasted."

    if command_id == "undo":
        system.undo()
        return "Undone."

    if command_id == "redo":
        system.redo()
        return "Redone."

    if command_id == "select_all":
        system.select_all()
        return "Everything selected."

    if command_id == "save_file":
        system.save_file()
        return "File saved."

    if command_id == "find":
        system.find_on_page()
        return "Find is open. What are you looking for?"

    if command_id == "type_text":
        text = params.get("text", "")
        if text:
            system.type_text(text)
            return f"Typed: {text}"
        return "What would you like me to type?"

    # ── WINDOW ───────────────────────────────────────────────────
    if command_id == "minimize":
        system.minimize_window()
        return "Window minimized."

    if command_id == "maximize":
        system.maximize_window()
        return "Window maximized."

    if command_id == "close_window":
        system.close_window()
        return "Closing this window."

    if command_id == "switch_window":
        system.switch_window()
        return "Switching windows."

    if command_id == "show_desktop":
        system.show_desktop()
        return "Here's your desktop."

    # ── VOLUME ───────────────────────────────────────────────────
    if command_id == "volume_up":
        system.increase_volume()
        return "Volume up."

    if command_id == "volume_down":
        system.decrease_volume()
        return "Volume down."

    if command_id == "mute":
        system.mute_volume()
        return "Muted."

    # ── POWER ────────────────────────────────────────────────────
    if command_id == "lock_screen":
        system.lock_screen()
        return "Locking your screen."

    if command_id == "shutdown":
        return "__SHUTDOWN__"

    if command_id == "restart":
        return "__RESTART__"

    # ── SESSION ──────────────────────────────────────────────────
    if command_id == "end_session":
        return "__END_SESSION__"

    return None