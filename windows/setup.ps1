# Windows side of the dotfiles: i3-like desktop (GlazeWM), PowerShell 7, terminal, vim, snippets, WSL settings.
# Run in PowerShell 7 from the repo:  pwsh -File windows\setup.ps1      (-SkipApps: only copy the configs)
# Apps needing admin (one UAC prompt): Everything, PowerToys, KDE Connect - see the end of this script.
param([switch]$SkipApps)
$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$repo = Split-Path $here -Parent
function Copy-To($src, $dst) { New-Item -ItemType Directory -Force (Split-Path $dst -Parent) | Out-Null; Copy-Item -LiteralPath $src -Destination $dst -Force -Recurse }

if (-not $SkipApps) {
    if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) { Invoke-RestMethod https://get.scoop.sh | Invoke-Expression }
    scoop bucket add extras; scoop bucket add nerd-fonts
    scoop install ripgrep fd fzf bat jq zoxide starship eza less 7zip vim yazi espanso `
        extras/glazewm extras/zebar extras/flow-launcher extras/copyq extras/altsnap nerd-fonts/JetBrainsMono-NF nerd-fonts/FiraCode-NF
}

# PowerShell 7 profile + prompt
Copy-To "$here\powershell\Microsoft.PowerShell_profile.ps1" "$HOME\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
Copy-To "$here\starship.toml" "$HOME\.config\starship.toml"

# vim: the Linux config from roles/linux-base + a Windows entry point
Copy-To "$repo\roles\linux-base\files\.vim" "$HOME\.vim"
Copy-To "$here\vim\_vimrc" "$HOME\_vimrc"

# GlazeWM (config generated from roles/linux-desktop/files/i3/config) + Zebar i3bar
Copy-To "$here\glazewm\gen_config.py" "$HOME\.glzr\glazewm\gen_config.py"
Copy-To "$here\glazewm\monitor_watch.py" "$HOME\.glzr\glazewm\monitor_watch.py"   # L/R workspaces follow the side monitors
Copy-To "$here\glazewm\quake.py" "$HOME\.glzr\glazewm\quake.py"                   # Win+` drop-down terminal
python -m pip install -q pyyaml
python "$HOME\.glzr\glazewm\gen_config.py"
Copy-To "$here\zebar\i3bar" "$HOME\.glzr\zebar\i3bar"
Set-Content -LiteralPath "$HOME\.glzr\zebar\settings.json" -Encoding utf8 -Value '{ "startupConfigs": [ { "pack": "i3bar", "widget": "bar", "preset": "default" } ] }'
$ws = New-Object -ComObject WScript.Shell
$lnk = $ws.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Startup')) 'GlazeWM.lnk'))
$lnk.TargetPath = "$HOME\scoop\apps\glazewm\current\glazewm.exe"; $lnk.WorkingDirectory = "$HOME\scoop\apps\glazewm\current"; $lnk.Save()

# Espanso (Scoop = portable mode): neutral snippets; work snippets go to match\private.yml (not in git)
$esp = "$HOME\scoop\persist\espanso\.espanso"
Copy-To "$here\espanso\config\default.yml" "$esp\config\default.yml"
python "$here\espanso\gen_espanso.py"
$lnk = $ws.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Startup')) 'espanso.lnk'))
$lnk.TargetPath = "$HOME\scoop\apps\espanso\current\espansod.exe"; $lnk.Arguments = 'daemon'; $lnk.WindowStyle = 7; $lnk.Save()

# CopyQ (Win+Shift+V) starts with Windows, i3bar colours
$cq = "$HOME\scoop\apps\copyq\current\copyq.exe"
Copy-To "$here\copyq\i3bar.ini" "$HOME\scoop\persist\copyq\config\copyq\themes\i3bar.ini"
if (Test-Path $cq) {
    if (-not (Get-Process copyq -ErrorAction SilentlyContinue)) { Start-Process $cq; Start-Sleep -Seconds 2 }
    & $cq config autostart true 2>$null
    & $cq loadTheme "$HOME\scoop\persist\copyq\config\copyq\themes\i3bar.ini" 2>$null
}

# Flow Launcher (Win+S): i3bar colours, Fira Code. It rewrites Settings.json on exit, so it is closed first
Copy-To "$here\flow-launcher\i3bar.xaml" "$HOME\scoop\persist\flow-launcher\UserData\Themes\i3bar.xaml"
$fs = "$HOME\scoop\persist\flow-launcher\UserData\Settings\Settings.json"
if (Test-Path $fs) {
    Get-Process Flow.Launcher -ErrorAction SilentlyContinue | Stop-Process -Force; Start-Sleep -Seconds 1
    $j = Get-Content $fs -Raw -Encoding UTF8 | ConvertFrom-Json
    $j.Theme = 'i3bar'; $j.ColorScheme = 'Dark'
    foreach ($k in 'QueryBoxFont', 'ResultFont', 'ResultSubFont') { $j.$k = 'FiraCode Nerd Font' }
    [IO.File]::WriteAllText($fs, ($j | ConvertTo-Json -Depth 50), (New-Object Text.UTF8Encoding($false)))
}

# AltSnap: Win + left mouse drags a window, Win + right mouse resizes it (i3 floating_modifier)
$as = "$HOME\scoop\persist\altsnap\AltSnap.ini"
if (Test-Path $as) {
    $t = [IO.File]::ReadAllText($as)
    [IO.File]::WriteAllText($as, ($t -replace '(?m)^Hotkeys=.*$', 'Hotkeys=5B 5C'), [Text.Encoding]::Unicode)
}
$lnk = $ws.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Startup')) 'AltSnap.lnk'))
$lnk.TargetPath = "$HOME\scoop\apps\altsnap\current\AltSnap.exe"; $lnk.WorkingDirectory = "$HOME\scoop\apps\altsnap\current"; $lnk.Save()

# WSL settings (mirrored localhost); the distro itself: wsl --install -d Ubuntu-24.04, then wsl.yml
Copy-To "$here\wslconfig" "$HOME\.wslconfig"

# Windows Terminal: PowerShell 7 default, the Terminator palette, Fira Code
$wt = Get-ChildItem "$env:LOCALAPPDATA\Packages" -Directory -Filter 'Microsoft.WindowsTerminal*' | Select-Object -First 1
if ($wt) {
    $sf = Join-Path $wt.FullName 'LocalState\settings.json'
    $j = Get-Content $sf -Raw -Encoding UTF8 | ConvertFrom-Json
    $scheme = Get-Content "$here\terminal\scheme.json" -Raw -Encoding UTF8 | ConvertFrom-Json
    $j | Add-Member -NotePropertyName schemes -NotePropertyValue (@(@($j.schemes) | Where-Object { $_ -and $_.name -ne $scheme.name }) + $scheme) -Force
    $set = @{ colorScheme = $scheme.name; scrollbarState = 'hidden'; historySize = 32767; padding = '8'; bellStyle = 'none'
              font = [pscustomobject]@{ face = 'FiraCode Nerd Font'; size = 12 } }
    foreach ($k in $set.Keys) { $j.profiles.defaults | Add-Member -NotePropertyName $k -NotePropertyValue $set[$k] -Force }
    $j | Add-Member -NotePropertyName copyOnSelect -NotePropertyValue $true -Force
    [IO.File]::WriteAllText($sf, ($j | ConvertTo-Json -Depth 20), (New-Object Text.UTF8Encoding($false)))
}

Write-Host 'Done. Admin apps (one UAC):  winget install voidtools.Everything Microsoft.PowerToys KDE.KDEConnect'
Write-Host 'Flow Launcher -> Explorer plugin: Index Search Engine and Path Enumeration = Everything.'
