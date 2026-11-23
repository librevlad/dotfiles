# Windows

The same habits on Windows (Excel keeps it there): `pwsh -File windows\setup.ps1`.

| What | Where it comes from |
|---|---|
| GlazeWM = i3 (`$mod` = Win, h/j/k/l, workspaces 1..0 on the primary monitor, L1/L2 on the left one, R1/R2 on the right one, TV1..0, resize mode; `monitor_watch.py` re-binds them when monitors are plugged in or out) | `glazewm/gen_config.py` (encodes `roles/linux-desktop/files/i3/config`) |
| Zebar bar = i3bar colours, `CPU / RAM / battery / dd.mm.yyyy HH:mm:ss`, plus what the taskbar gave: tray icons (clicks as on the taskbar), volume (wheel / click = mute), Wi-Fi (click = network list), now playing (click = pause), date click = notifications, CPU/RAM click = Task Manager (red above 85%) | `zebar/i3bar` |
| Flow Launcher (Win+S) and CopyQ (Win+Shift+V) in the i3bar colours | `flow-launcher/i3bar.xaml`, `copyq/i3bar.ini` |
| AltSnap: Win + left mouse drags a window, Win + right mouse resizes it (i3 `floating_modifier`) | `setup.ps1` (`Hotkeys=5B 5C`) |
| PowerShell 7: starship (fish colours), zoxide, fzf Ctrl+R/T, the fish functions (ga gs gc gl push nah c up down k rf n pa ...) | `powershell/`, `starship.toml` |
| Windows Terminal: Terminator palette, Fira Code | `terminal/scheme.json` |
| vim: `roles/linux-base/files/.vim` + Windows fixes | `vim/_vimrc` |
| Espanso: `:date`, `:time` in any keyboard layout | `espanso/` (work snippets: `match/private.yml`, kept out of git) |
| Projects: `C:\work` = `/work` in Ubuntu (`cdw` in PowerShell and fish) | `powershell/`, `../wsl.yml` |
| WSL2: mirrored localhost | `wslconfig`; Ubuntu itself: `../wsl.yml` |

Look: gaps 20, Windows 11 rounded corners with the system window shadows (i3 had square ones).

Differences from i3: Win+L is the Windows lock (focus right is also Win+Right), no tabbed layout, Win+Space switches
the keyboard layout, no i3 `assign`: every window opens on the workspace you are on (tying apps to workspaces made
some of them seem to vanish). Extras not in i3: Win+Shift+V clipboard history (CopyQ); standard Windows dialogs are
left alone (moving them between monitors of different scale cut them off). Win+Alt+E = File Explorer (Win+E is
workspace R1, as in i3). Win+Shift+Enter = terminal in WSL
Ubuntu. Win+` = drop-down terminal (i3 scratchpad style, `glazewm/quake.py`): one floating Windows Terminal window
titled "Quake" at the top of the focused monitor; the key brings it to the current workspace or hides it.
Win+- = minimized windows back (i3 "scratchpad show", `glazewm/unminimize.py`): GlazeWM drops a minimized window
from the layout and there is no taskbar to click, so the key restores the minimized windows of the current
workspace, or, if there are none, brings the minimized windows of other workspaces here.

Win never opens Start: GlazeWM swallows the key of its Win+key bindings, so Windows saw a lone Win press and opened
Start on release (glzr-io/glazewm#1215; always with Win+`). `glazewm/no-start-menu.ahk` (AutoHotkey v2, from
shell:startup) sends a dummy key the moment Win goes down. Start: Ctrl+Esc; apps: Win+S.

## WSL

```
wsl --install -d Ubuntu-24.04        # then create the user librevlad
wsl -u root -- bash -lc "apt-get install -y ansible-core git && git clone <this repo> /home/librevlad/dotfiles && cd /home/librevlad/dotfiles && ansible-playbook -i localhost, -c local wsl.yml -e user=librevlad"
```

`wsl.yml` = role `linux-base` for WSL (no `velociraptor` user, broken fisherman symlinks skipped, fzf/z from packages),
plus `--tags extras`: ranger config, `wsl/tmux.conf` (tmux 3.x version), `~/docs` -> Windows documents.

## Without the taskbar

Settings -> Personalization -> Taskbar -> Taskbar behaviors -> Automatically hide the taskbar. The bar sits at the bottom like i3bar (the hidden taskbar shows up over it only when the mouse touches the very edge). Windows by name: PowerToys Command Palette, Win+Alt+Space. In PowerToys turn FancyZones off (it fights GlazeWM); Text Extractor = Win+Shift+T.

Optional, stronger shadows: Windhawk + mod "Windows Shadows Tuner" (native-shadow-tuner). It hooks dwm.exe, so add
`dwm.exe` to Windhawk -> Settings -> Advanced settings -> More advanced settings (registry:
`HKLM\SOFTWARE\Windhawk\Engine\Settings`, `Include`, pipe-separated). Shadows hardly show on a dark wallpaper.

Windows' own Win+letter shortcuts that the i3 bindings use (otherwise Win+S also opens Start):
`HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced`, `DisabledHotkeys` = `SCTQAEDBVHKF`, then restart Explorer.
