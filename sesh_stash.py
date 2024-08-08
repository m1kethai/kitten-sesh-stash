import os
import json
import time
from kitty.boss import Boss, os_window as current_os_window

# Configuration variables
MAX_SAVED_SESSIONS = 5
SESSION_STASH_DIR = os.path.expanduser("~/.config/kitty/.session_stash/")

def main(args):
    action = args[1] if len(args) > 1 else None
    if action in ["restore", "resto", "r"]:
        restore_state()
    elif action is None or action in ["stash", "save", "s"]:
        save_state()
    else:
        print("Usage: `[kitty +]kitten sesh_stash [restore|resto|r|save|s]`")

def save_state():
    boss = Boss()
    os_windows = boss.os_windows
    session_data = []

    for os_window in os_windows:
        os_window_data = {
            "id": os_window.id,
            "tabs": [],
        }
        for tab in os_window.tabs:
            tab_data = {
                "id": tab.id,
                "layout": tab.layout,
                "windows": [],
            }
            for window in tab.windows:
                window_data = {
                    "id": window.id,
                    "cmdline": window.cmdline,
                    "cwd": window.cwd,
                    "title": window.title,
                }
                tab_data["windows"].append(window_data)
            os_window_data["tabs"].append(tab_data)
        session_data.append(os_window_data)

    # Create the directory if it doesn't exist
    os.makedirs(SESSION_STASH_DIR, exist_ok=True)

    # Create a timestamped filename
    timestamp = time.strftime("%Y%m%d%H%M%S")
    session_file = os.path.join(SESSION_STASH_DIR, f"kitty_session_{timestamp}.json")

    # Write session data to the file
    with open(session_file, "w") as f:
        json.dump(session_data, f, indent=4)

    print(f"Kitty session saved: {session_file}")

    # Clean up old sessions if we exceed the maximum allowed
    cleanup_sessions()

def restore_state():
    latest_session = max(
        (os.path.join(SESSION_STASH_DIR, f) for f in os.listdir(SESSION_STASH_DIR)),
        key=os.path.getctime,
        default=None
    )

    if not latest_session:
        print("No session files found.")
        return

    with open(latest_session, "r") as f:
        session_data = json.load(f)

    for os_window_data in session_data:
        for tab_data in os_window_data["tabs"]:
            for window_data in tab_data["windows"]:
                cmd = f'kitty @ launch --type=window --cwd="{window_data["cwd"]}" --title="{window_data["title"]}" {window_data["cmdline"]}'
                os.system(cmd)

    print(f"Kitty session restored: {latest_session}")

def cleanup_sessions():
    session_files = sorted(
        (os.path.join(SESSION_STASH_DIR, f) for f in os.listdir(SESSION_STASH_DIR) if f.endswith(".json")),
        key=os.path.getctime
    )

    # Remove oldest files if we exceed the maximum number of saved sessions
    if len(session_files) > MAX_SAVED_SESSIONS:
        for session_file in session_files[:-MAX_SAVED_SESSIONS]:
            os.remove(session_file)
            print(f"Removed old session file: {session_file}")