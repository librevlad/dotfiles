"""Win+- : bring minimized windows back (i3 "scratchpad show" style).

GlazeWM takes a minimized window out of the layout, and with the bar instead of a taskbar there is no obvious way
back (23.11.2026: the Claude window got minimized and "could not be found"). Pressing the key:
  - minimized windows on the focused workspace -> restored to their previous state, the last one focused;
  - none here -> minimized windows from other workspaces are moved here and restored.
"""
import json
import os
import subprocess

GLAZE = os.path.join(os.path.expanduser("~"), "scoop", "apps", "glazewm", "current", "cli", "glazewm.exe")
NO_WINDOW = 0x08000000   # CREATE_NO_WINDOW: no console flash from pythonw


def glaze(*args):
    return subprocess.run([GLAZE, *args], capture_output=True, text=True, encoding="utf-8",
                          creationflags=NO_WINDOW).stdout


def main():
    mons = json.loads(glaze("query", "monitors"))["data"]["monitors"]
    focus_ws = None
    for m in mons:
        for w in m.get("children", []):
            if w.get("hasFocus") or (focus_ws is None and m.get("hasFocus") and w.get("isDisplayed")):
                focus_ws = w
    if focus_ws is None:
        return
    here, elsewhere = [], []

    def walk(node, ws):
        for c in node.get("children", []):
            if c.get("type") == "window" and (c.get("state") or {}).get("type") == "minimized":
                (here if ws["id"] == focus_ws["id"] else elsewhere).append(c)
            walk(c, ws)

    for m in mons:
        for w in m.get("children", []):
            walk(w, w)
    restore = here
    if not restore:
        for win in elsewhere:
            glaze("command", "--id", win["id"], "move", "--workspace", focus_ws["name"])
        restore = elsewhere
    for win in restore:
        glaze("command", "--id", win["id"], "toggle-minimized")
    if restore:
        glaze("command", "focus", "--container-id", restore[-1]["id"])


if __name__ == "__main__":
    main()
