"""Generate ~/.glzr/glazewm/config.yaml from the user's i3 config (dotfiles/roles/linux-desktop/files/i3/config)."""
import io
import os

import yaml

HOME = os.path.expanduser("~")
FLOW = HOME + r"\scoop\apps\flow-launcher\current\Flow.Launcher.exe"
ZEBAR = HOME + r"\scoop\apps\zebar\current\zebar.exe"
PYW = HOME + r"\AppData\Local\Programs\Python\Python313\pythonw.exe"
WATCH = os.path.join(HOME, ".glzr", "glazewm", "monitor_watch.py")  # keeps workspaces on their i3 outputs
OUT = os.path.join(HOME, ".glzr", "glazewm", "config.yaml")

main = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']   # i3: " 1 " .. " 0 " (browser, ide, term, music, chat, files, 7..9, ten)
side = {'q': 'L1', 'a': 'L2', 'e': 'R1', 'd': 'R2'}         # i3: left / right monitor workspaces
tv = ['TV' + d for d in main]                                # i3: $mod+Mod1+digit
dirs = [('left', 'h', 'left'), ('down', 'j', 'down'), ('up', 'k', 'up'), ('right', 'l', 'right')]


def monitor_layout():
    """i3 outputs -> GlazeWM monitor indices (0 = leftmost). Centre = the Windows primary monitor (i3: $centralMoni),
    left / right = its neighbours (i3: $leftMoni / $rightMoni), TV = any further monitor. None = not connected."""
    import ctypes
    import ctypes.wintypes as w
    user32 = ctypes.windll.user32

    class MONITORINFO(ctypes.Structure):
        _fields_ = [('cbSize', w.DWORD), ('rcMonitor', w.RECT), ('rcWork', w.RECT), ('dwFlags', w.DWORD)]

    found = []
    proc = ctypes.WINFUNCTYPE(ctypes.c_int, w.HMONITOR, w.HDC, ctypes.POINTER(w.RECT), w.LPARAM)

    def cb(h, _dc, _r, _l):
        mi = MONITORINFO()
        mi.cbSize = ctypes.sizeof(mi)
        user32.GetMonitorInfoW(h, ctypes.byref(mi))
        found.append((mi.rcMonitor.left, mi.rcMonitor.top, bool(mi.dwFlags & 1)))
        return 1

    user32.EnumDisplayMonitors(None, None, proc(cb), 0)
    found.sort()
    n = len(found)
    centre = next((i for i, m in enumerate(found) if m[2]), 0)
    left = centre - 1 if centre >= 1 else None
    right = centre + 1 if centre + 1 < n else None
    rest = [i for i in range(n) if i not in (centre, left, right)]
    return {'count': n, 'centre': centre if n > 1 else None, 'left': left, 'right': right, 'tv': rest[0] if rest else None}


MON = monitor_layout()


def ws(name, where):
    """A workspace, bound to its i3 output when that monitor is connected."""
    idx = MON[where]
    return {'name': name, 'bind_to_monitor': idx} if idx is not None else {'name': name}

L = []


def kb(cmds, *keys):
    L.append({'commands': cmds if isinstance(cmds, list) else [cmds], 'bindings': list(keys)})


QUAKE = os.path.join(HOME, ".glzr", "glazewm", "quake.py")             # drop-down terminal toggle
UBUNTU = '{b40bed0d-cfad-5ecf-a53d-e1c7a438aa67}'                      # Windows Terminal profile "Ubuntu (fish)"
kb('shell-exec wt.exe', 'lwin+enter')                                  # $mod+Return exec terminator
kb(f'shell-exec wt.exe -p {UBUNTU}', 'lwin+shift+enter')               # not in i3: the same, in WSL Ubuntu
kb(f'shell-exec {PYW} {QUAKE}', 'lwin+oem_tilde')                          # not in i3: drop-down terminal (scratchpad style)
kb('close', 'lwin+c')                                                  # $mod+c kill
kb('shell-exec ' + FLOW, 'lwin+s')                                     # $mod+s exec rofi -show run
kb('shell-exec rundll32.exe user32.dll,LockWorkStation', 'lwin+t')     # $mod+t lock.sh
for d, k, arrow in dirs:
    kb(f'focus --direction {d}', f'lwin+{k}', f'lwin+{arrow}')        # Win+L is the Windows lock: arrows as backup
for d, k, arrow in dirs:
    kb(f'move --direction {d}', f'lwin+shift+{k}', f'lwin+alt+{k}', f'lwin+shift+{arrow}')
kb('set-tiling-direction horizontal', 'lwin+b')                        # split h
kb('set-tiling-direction vertical', 'lwin+v')                          # split v
kb('toggle-tiling-direction', 'lwin+y')                                # layout toggle split
kb('toggle-fullscreen', 'lwin+f')
kb('toggle-floating --centered', 'lwin+shift+space')
for d in main:
    kb(f'focus --workspace {d}', f'lwin+{d}')
for k, name in side.items():
    kb(f'focus --workspace {name}', f'lwin+{k}')
for d, name in zip(main, tv):
    kb(f'focus --workspace {name}', f'lwin+alt+{d}')
kb('focus --prev-active-workspace-on-monitor', 'lwin+shift+o')         # workspace prev_on_output
kb('focus --next-active-workspace-on-monitor', 'lwin+shift+p')         # workspace next_on_output
for d in main:
    kb(f'move --workspace {d}', f'lwin+shift+{d}')
for k, name in side.items():
    kb(f'move --workspace {name}', f'lwin+shift+{k}')
for d, name in zip(main, tv):
    kb(f'move --workspace {name}', f'lwin+alt+shift+{d}')
kb('wm-reload-config', 'lwin+shift+c')                                 # reload
kb('wm-redraw', 'lwin+shift+g')                                        # restart
kb('wm-exit', 'lwin+shift+w')                                          # exit
kb('wm-enable-binding-mode --name resize', 'lwin+shift+r')             # mode "resize"
# not in i3: clipboard history (Win+V became split v, as in i3)
kb('shell-exec ' + HOME + r'\scoop\apps\copyq\current\copyq.exe toggle', 'lwin+shift+v')
# not in i3: File Explorer on the current workspace (Win+E is workspace R1, as in i3)
kb('shell-exec explorer.exe', 'lwin+alt+e')

# i3 "assign" + follow: new windows of these apps go to their workspace and focus follows them (i3 names: 1 browser, 2 ide, 3 term, 5 chat, 6 files)
ASSIGN = [
    ('1', [{'window_process': {'regex': '^(chrome|firefox|msedge)$'}}]),
    ('2', [{'window_process': {'regex': '^(Code|phpstorm64)$'}},
           # the Claude desktop app's main window: closing it hides it to the tray, and the tray icon brings it back
           # on whatever workspace is focused, so it seemed to vanish from 2
           {'window_process': {'equals': 'claude'}, 'window_title': {'equals': 'Claude'}}]),
    # terminal and Explorer are NOT assigned: they are needed on any workspace (user, 22.11.2026)
    ('5', [{'window_process': {'equals': 'Telegram'}}]),
    ('7', [{'window_process': {'equals': 'EXCEL'}, 'window_class': {'equals': 'XLMAIN'}},
           {'window_process': {'equals': 'WINWORD'}, 'window_class': {'equals': 'OpusApp'}}]),
]

resize = [{'commands': [c], 'bindings': k} for c, k in [
    ('resize --width -10%', ['h', 'left']), ('resize --height +10%', ['j', 'down']),
    ('resize --height -10%', ['k', 'up']), ('resize --width +10%', ['l', 'right'])]]
resize.append({'commands': ['wm-disable-binding-mode --name resize'], 'bindings': ['enter', 'escape']})

no_effects = {'hide_title_bar': {'enabled': False}, 'corner_style': {'enabled': True, 'style': 'rounded'}}  # Windows 11 rounded corners + its shadows
cfg = {
    'general': {
        'startup_commands': ['shell-exec ' + ZEBAR, 'shell-exec ' + FLOW, f'shell-exec {PYW} {WATCH}'],
        'shutdown_commands': ['shell-exec taskkill /IM zebar.exe /F'],
        'config_reload_commands': [],
        'focus_follows_cursor': True,            # i3 default focus_follows_mouse yes
        'toggle_workspace_on_refocus': True,     # workspace_auto_back_and_forth yes
        'cursor_jump': {'enabled': True, 'trigger': 'monitor_focus'},
        'hide_method': 'cloak',
        'show_all_in_taskbar': False,
    },
    'gaps': {'scale_with_dpi': True, 'inner_gap': '20px',          # gaps inner 20
             'outer_gap': {'top': '20px', 'right': '20px', 'bottom': '52px', 'left': '20px'}},  # bottom: 20 + the 32px bar (i3bar is at the bottom)
    'window_effects': {                                              # border pixel 0
        'focused_window': {'border': {'enabled': False, 'color': '#336699'}, **no_effects,
                           'transparency': {'enabled': False, 'opacity': '95%'}},
        'other_windows': {'border': {'enabled': False, 'color': '#484e50'}, **no_effects,
                          'transparency': {'enabled': False, 'opacity': '0%'}},
    },
    'window_behavior': {'initial_state': 'tiling', 'state_defaults': {
        'floating': {'centered': True, 'shown_on_top': False},
        'fullscreen': {'maximized': False, 'shown_on_top': False}}},
    'workspaces': [ws(n, 'centre') for n in main] + [ws(n, 'left') for n in ('L1', 'L2')]
                  + [ws(n, 'right') for n in ('R1', 'R2')] + [ws(n, 'tv') for n in tv],
    'window_rules': [
        {'commands': ['ignore'], 'match': [
            {'window_process': {'equals': 'zebar'}},
            {'window_process': {'equals': 'Flow.Launcher'}},
            {'window_title': {'regex': '[Pp]icture.in.[Pp]icture'},
             'window_class': {'regex': 'Chrome_WidgetWin_1|MozillaDialogClass'}},
            {'window_process': {'equals': 'PowerToys'}, 'window_class': {'regex': r'HwndWrapper\[PowerToys\.PowerAccent.*?\]'}},
            {'window_title': {'equals': 'Command Palette'}, 'window_class': {'equals': 'WinUIDesktopWin32WindowClass'}},
            # Office: only main windows tile; Save As, macro and print dialogs stay as they are
            {'window_process': {'equals': 'EXCEL'}, 'window_class': {'not_regex': 'XLMAIN'}},
            {'window_process': {'equals': 'WINWORD'}, 'window_class': {'not_regex': 'OpusApp'}},
            {'window_process': {'equals': 'POWERPNT'}, 'window_class': {'not_regex': 'PPTFrameClass'}},
        ]},
        {'commands': ['ignore'], 'match': [{'window_process': {'equals': 'espansod'}}]},  # snippet popups
        # Standard Windows dialogs (Save As, Open, properties, message boxes): left to Windows. Floating + centring
        # them moved them between monitors of different scale (100/150/200%) and they came out cut off.
        {'commands': ['ignore'], 'match': [{'window_class': {'equals': '#32770'}}]},
        {'commands': ['set-floating --centered'], 'match': [
            {'window_process': {'equals': 'Taskmgr'}},
            {'window_process': {'equals': 'copyq'}},         # clipboard history (Win+Shift+V)
            {'window_process': {'equals': 'Everything'}},
        ]},
        # the Win+` drop-down terminal (quake.py places it); the title arrives just after creation -> also on title_change
        {'commands': ['set-floating --shown-on-top --centered=false'], 'on': ['manage', 'title_change'],
         'match': [{'window_process': {'equals': 'WindowsTerminal'}, 'window_title': {'equals': 'Quake'}}]},
    # follow the window: otherwise a taskbar click opens it on a hidden workspace and seems to do nothing
    ] + [{'commands': [f'move --workspace {ws}', f'focus --workspace {ws}'], 'match': m} for ws, m in ASSIGN],
    'binding_modes': [{'name': 'resize', 'keybindings': resize}],
    'keybindings': L,
}
class NoAliasDumper(yaml.SafeDumper):
    """Plain YAML for GlazeWM: no &anchors / *aliases for shared dicts."""
    def ignore_aliases(self, data):
        return True


head = """# GlazeWM = ~/dotfiles/roles/linux-desktop/files/i3/config on Windows (generated 22.11.2026 by ~/.glzr/glazewm/gen_config.py; edit that and re-run).
# $mod = Win. Workspaces: 1..0 (Win+digit), L1 L2 (Win+Q/A), R1 R2 (Win+E/D), TV1..TV0 (Win+Alt+digit).
# Differences from i3: Win+L is the Windows lock and cannot be taken -> focus right is also Win+Right;
# arrows added for focus/move; no tabbed layout (Win+W); no drag with floating_modifier.
# Win+Space stays the keyboard layout switch. Reload after edits: Win+Shift+C.
"""
io.open(OUT, 'w', encoding='utf-8', newline='\n').write(
    head + yaml.dump(cfg, Dumper=NoAliasDumper, allow_unicode=True, sort_keys=False, width=200))
d = yaml.safe_load(io.open(OUT, encoding='utf-8'))
keys = [b for k in d['keybindings'] for b in k['bindings']]
print('monitors:', MON)
print('keybindings:', len(d['keybindings']), 'keys:', len(keys),
      'duplicates:', sorted({k for k in keys if keys.count(k) > 1}))
