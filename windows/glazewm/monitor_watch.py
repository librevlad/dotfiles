"""Keeps GlazeWM workspaces on their i3 outputs: 1..0 on the centre (primary) monitor, L1/L2 on the left one,
R1/R2 on the right one, TV* on a further one. Started by GlazeWM (startup_commands); on start and on every
monitor_added / monitor_removed / monitor_updated it regenerates config.yaml (gen_config.py), reloads it and moves
active workspaces that sit on the wrong monitor. Exits when GlazeWM exits.
    python monitor_watch.py --once     just do one pass (for testing)
"""
import json
import os
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
G = os.path.expanduser(r"~\scoop\apps\glazewm\current\cli\glazewm.exe")
GEN = os.path.join(HERE, "gen_config.py")
LOG = os.path.join(HERE, "monitor_watch.log")
NOWIN = 0x08000000  # CREATE_NO_WINDOW


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%d.%m %H:%M:%S ") + msg + "\n")


def run(*args):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", creationflags=NOWIN)


def query(kind):
    return json.loads(run(G, "query", kind).stdout)["data"]


def monitor_signature():
    """What matters for workspace placement: the set of monitors and their geometry."""
    try:
        return tuple(sorted((m["x"], m["y"], m["width"], m["height"]) for m in query("monitors")["monitors"]))
    except Exception:
        return None


def focused_workspace():
    try:
        return next((w["name"] for m in query("monitors")["monitors"] for w in m["children"] if w.get("hasFocus")), None)
    except Exception:
        return None


def relocate():
    gen = run(sys.executable, GEN)
    log("gen: " + " | ".join(l for l in gen.stdout.splitlines() if l.startswith("monitors")) + (gen.stderr.strip()[:300]))
    run(G, "command", "wm-reload-config")
    time.sleep(1)
    import yaml
    with open(os.path.join(HERE, "config.yaml"), encoding="utf-8") as f:
        bound = {w["name"]: w.get("bind_to_monitor") for w in yaml.safe_load(f)["workspaces"]}
    monitors = sorted(query("monitors")["monitors"], key=lambda m: (m["x"], m["y"]))
    focused = next((w["name"] for m in monitors for w in m["children"] if w.get("hasFocus")), None)
    moved = []
    for idx, m in enumerate(monitors):
        for w in m["children"]:
            target = bound.get(w["name"])
            if target is None or target == idx or target >= len(monitors):
                continue
            run(G, "command", "focus", "--workspace", w["name"])
            direction = "right" if target > idx else "left"
            for _ in range(abs(target - idx)):
                run(G, "command", "move-workspace", "--direction", direction)
            moved.append(f"{w['name']}: {idx}->{target}")
    # Give the focus back only if a move took it away: with toggle_workspace_on_refocus (i3 back_and_forth)
    # focusing the workspace that already has the focus jumps to the PREVIOUS one. Monitors that sleep send
    # monitor_updated every ~30 s, and refocusing on each pass flipped the screen between two workspaces
    # (23.11.2026: 2 <-> 6 for an hour while the user was away).
    if focused and focused_workspace() != focused:
        run(G, "command", "focus", "--workspace", focused)
    log("moved: " + (", ".join(moved) or "nothing"))


def main():
    if "--once" in sys.argv:
        relocate()
        return
    time.sleep(3)  # let GlazeWM finish starting
    relocate()
    last_sig = [monitor_signature()]
    sub = subprocess.Popen([G, "sub", "-e", "monitor_added", "monitor_removed", "monitor_updated"],
                           stdout=subprocess.PIPE, text=True, encoding="utf-8", creationflags=NOWIN)
    timer = None
    quiet_until = [0.0]

    def pass_():
        # monitor_updated also fires without any real change (sleeping monitors: every ~30 s): act only when the
        # set of monitors or their geometry changed
        sig = monitor_signature()
        if sig is not None and sig == last_sig[0]:
            return
        relocate()
        last_sig[0] = monitor_signature()
        quiet_until[0] = time.time() + 5  # our own workspace moves must not trigger another pass

    for line in sub.stdout:  # one JSON line per event; several arrive together when a monitor is plugged in
        if '"eventType":"monitor_' not in line or time.time() < quiet_until[0]:
            continue
        if timer:
            timer.cancel()
        timer = threading.Timer(2.0, pass_)
        timer.start()
    log("GlazeWM gone, watcher exits")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # never die silently
        log(f"error: {e!r}")
        raise
