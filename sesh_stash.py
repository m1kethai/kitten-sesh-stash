import os
import json
from kitty.boss import Boss
from kitty.boss import os_window as current_os_window

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

    with open(os.path.expanduser("~/.config/kitty/.session_stash/"), "w") as f:
        json.dump(session_data, f, indent=4)

    print("Kitty session saved.")

def restore_state():
    with open(os.path.expanduser("~/.config/kitty/.session_stash/"), "r") as f:
        session_data = json.load(f)

    for os_window_data in session_data:
        os_window_id = os_window_data["id"]
        for tab_data in os_window_data["tabs"]:
            for window_data in tab_data["windows"]:
                cmd = f'kitty @ launch --type=window --cwd="{window_data["cwd"]}" --title="{window_data["title"]}" {window_data["cmdline"]}'
                os.system(cmd)

    print("Kitty session restored.")

def handle_result(args, result, target_window_id, boss):
    pass

def handle_result(args, result, target_window_id, boss):
    pass

def main():
    save_state()

def main(args):
    pass
