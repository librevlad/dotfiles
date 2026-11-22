# Windows

The same habits on Windows (Excel keeps it there): `pwsh -File windows\setup.ps1`.

| What | Where it comes from |
|---|---|
| GlazeWM = i3 (`$mod` = Win, h/j/k/l, workspaces 1..0 on the primary monitor, L1/L2 on the left one, R1/R2 on the right one, TV1..0, resize mode; `monitor_watch.py` re-binds them when monitors are plugged in or out) | `glazewm/gen_config.py` (encodes `roles/linux-desktop/files/i3/config`) |
| Zebar bar = i3bar colours, `battery / dd.mm.yyyy HH:mm:ss`, plus what the taskbar gave: tray icons (clicks as on the taskbar), volume (wheel / click = mute), Wi-Fi (click = network list), now playing (click = pause), date click = notifications | `zebar/i3bar` |
| PowerShell 7: starship (fish colours), zoxide, fzf Ctrl+R/T, the fish functions (ga gs gc gl push nah c up down k rf n pa ...) | `powershell/`, `starship.toml` |
| Windows Terminal: Terminator palette, Fira Code | `terminal/scheme.json` |
| vim: `roles/linux-base/files/.vim` + Windows fixes | `vim/_vimrc` |
| Espanso: `:date`, `:time` in any keyboard layout | `espanso/` (work snippets: `match/private.yml`, kept out of git) |
| Projects: `C:\work` = `/work` in Ubuntu (`cdw` in PowerShell and fish) | `powershell/`, `../wsl.yml` |
| WSL2: mirrored localhost | `wslconfig`; Ubuntu itself: `../wsl.yml` |

Look: gaps 20, Windows 11 rounded corners with the system window shadows (i3 had square ones).

Differences from i3: Win+L is the Windows lock (focus right is also Win+Right), no tabbed layout, Win+Space switches
the keyboard layout. Extras not in i3: Win+Shift+V clipboard history (CopyQ); windows go to their workspaces
(browser 1, VS Code 2, terminal 3, Telegram 5, Explorer 6, Excel/Word 7), and focus follows them.

## WSL

```
wsl --install -d Ubuntu-24.04        # then create the user librevlad
wsl -u root -- bash -lc "apt-get install -y ansible-core git && git clone <this repo> /home/librevlad/dotfiles && cd /home/librevlad/dotfiles && ansible-playbook -i localhost, -c local wsl.yml -e user=librevlad"
```

`wsl.yml` = role `linux-base` for WSL (no `velociraptor` user, broken fisherman symlinks skipped, fzf/z from packages),
plus `--tags extras`: ranger config, `wsl/tmux.conf` (tmux 3.x version), `~/docs` -> Windows documents.

## Without the taskbar

Settings -> Personalization -> Taskbar -> Taskbar behaviors -> Automatically hide the taskbar. The bar sits at the bottom like i3bar (the hidden taskbar shows up over it only when the mouse touches the very edge). Windows by name: PowerToys Command Palette, Win+Alt+Space. In PowerToys turn FancyZones off (it fights GlazeWM); Text Extractor = Win+Shift+T.
