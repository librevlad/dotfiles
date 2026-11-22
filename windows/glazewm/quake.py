"""Win+` drop-down terminal for GlazeWM (i3 scratchpad style).

One Windows Terminal window titled "Quake" (focus mode, no tabs). Pressing the key:
  - no such window      -> start it and drop it down at the top of the focused monitor;
  - it has the focus    -> hide it (minimize);
  - otherwise           -> bring it to the focused workspace, drop it down and focus it.
The window rule in config.yaml makes it floating so GlazeWM does not tile it.
"""
import json
import os
import subprocess
import time

HOME = os.path.expanduser("~")
GLAZE = os.path.join(HOME, "scoop", "apps", "glazewm", "current", "cli", "glazewm.exe")
TITLE = "Quake"
HEIGHT = 0.45            # share of the monitor height
NO_WINDOW = 0x08000000   # CREATE_NO_WINDOW: no console flash from pythonw


def glaze(*args):
    r = subprocess.run([GLAZE, *args], capture_output=True, text=True, encoding="utf-8", creationflags=NO_WINDOW)
    return r.stdout


def tree():
    """Monitors with their workspaces; the quake window and the workspace it is on."""
    mons = json.loads(glaze("query", "monitors"))["data"]["monitors"]
    focus_ws = focus_mon = quake = quake_ws = None

    def walk(node, ws):
        nonlocal quake, quake_ws
        for c in node.get("children", []):
            if c.get("type") == "window" and c.get("processName") == "WindowsTerminal" and c.get("title") == TITLE:
                quake, quake_ws = c, ws
            walk(c, ws)

    for m in mons:
        for w in m.get("children", []):
            if w.get("hasFocus") or (focus_ws is None and m.get("hasFocus") and w.get("isDisplayed")):
                focus_ws, focus_mon = w, m
            walk(w, w)
    return focus_ws, focus_mon, quake, quake_ws


def drop(win_id, ws, mon):
    """Floating, on top, full width at the top of the monitor (gaps as in the config: 20px scaled)."""
    gap = round(20 * (mon.get("scaleFactor") or 1))
    x, y = mon["x"] + gap, mon["y"] + gap
    w, h = mon["width"] - 2 * gap, round(mon["height"] * HEIGHT)
    glaze("command", "--id", win_id, "move", "--workspace", ws["name"])
    # set-floating restores it from minimized; it ignores --x-pos/--width for a window that is already floating,
    # so size and position go separately
    glaze("command", "--id", win_id, "set-floating", "--centered=false")
    glaze("command", "--id", win_id, "size", "--width", f"{w}px", "--height", f"{h}px")
    glaze("command", "--id", win_id, "position", "--x-pos", str(x), "--y-pos", str(y))
    glaze("command", "focus", "--container-id", win_id)


def main():
    ws, mon, quake, quake_ws = tree()
    if quake is None:
        subprocess.Popen(["wt.exe", "-w", "quake", "--focus", "new-tab", "--title", TITLE, "--suppressApplicationTitle"],
                         creationflags=NO_WINDOW)
        for _ in range(50):          # up to 5 s for the window to appear and get its title
            time.sleep(0.1)
            ws, mon, quake, quake_ws = tree()
            if quake is not None:
                break
        if quake is None or ws is None:
            return
        drop(quake["id"], ws, mon)
        return
    if quake.get("hasFocus") and quake["state"]["type"] != "minimized":
        glaze("command", "--id", quake["id"], "set-minimized")
        return
    if ws is not None:
        drop(quake["id"], ws, mon)


if __name__ == "__main__":
    main()
