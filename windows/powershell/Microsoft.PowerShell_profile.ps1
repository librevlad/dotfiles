# PowerShell 7 profile: Linux-like interactive shell (22.11.2026). Only for interactive sessions.
# Tools come from Scoop: starship (prompt), zoxide (z), fzf (Ctrl+R / Ctrl+T), eza, bat, ripgrep, fd.

[Console]::InputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
$OutputEncoding = [Text.UTF8Encoding]::new($false)

# bash-like line editing: Ctrl+A/E/U/K/W, Tab menu, history suggestions
Set-PSReadLineOption -EditMode Emacs -BellStyle None -HistoryNoDuplicates
if (-not [Console]::IsOutputRedirected) { Set-PSReadLineOption -PredictionSource History -PredictionViewStyle InlineView }
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward

# Ctrl+R: fuzzy history search, Ctrl+T: insert a file path (fzf)
if (Get-Command fzf -ErrorAction SilentlyContinue) {
    Set-PSReadLineKeyHandler -Chord 'Ctrl+r' -ScriptBlock {
        $hist = [Microsoft.PowerShell.PSConsoleReadLine]::GetHistoryItems() | ForEach-Object CommandLine
        [array]::Reverse($hist)
        $sel = $hist | Select-Object -Unique | fzf --height 40% --reverse --no-sort --query ([Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState)
        if ($sel) { [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine(); [Microsoft.PowerShell.PSConsoleReadLine]::Insert($sel) }
    }
    Set-PSReadLineKeyHandler -Chord 'Ctrl+t' -ScriptBlock {
        $sel = if (Get-Command fd -ErrorAction SilentlyContinue) { fd --type f --hidden --exclude .git | fzf --height 40% --reverse } else { fzf --height 40% --reverse }
        if ($sel) { [Microsoft.PowerShell.PSConsoleReadLine]::Insert($sel) }
    }
}

# Linux habits
foreach ($a in 'ls', 'cat') { if (Test-Path "Alias:$a") { Remove-Item "Alias:$a" -Force } }
if (Get-Command eza -ErrorAction SilentlyContinue) {
    function ls { eza --group-directories-first --icons=auto @args }
    function ll { eza -l --group-directories-first --icons=auto --git @args }
    function la { eza -la --group-directories-first --icons=auto --git @args }
    function lt { eza --tree --level=2 --icons=auto @args }
}
if (Get-Command bat -ErrorAction SilentlyContinue) { function cat { bat --paging=never --style=plain @args } }
if (Get-Command rg -ErrorAction SilentlyContinue) { Set-Alias grep rg }
function which($name) { Get-Command $name -All | ForEach-Object { if ($_.Source) { $_.Source } else { $_.Definition } } }
function touch($path) { if (Test-Path -LiteralPath $path) { (Get-Item -LiteralPath $path).LastWriteTime = Get-Date } else { New-Item -ItemType File -Path $path | Out-Null } }
function mkcd($path) { New-Item -ItemType Directory -Force -Path $path | Out-Null; Set-Location $path }
function open($path = '.') { Invoke-Item $path }        # xdg-open
function .. { Set-Location .. }
function ... { Set-Location ../.. }
function export { param([Parameter(ValueFromRemainingArguments)]$kv) foreach ($p in $kv) { $n, $v = $p -split '=', 2; Set-Item "env:$n" $v } }
Set-Alias -Name g -Value git

# ---- functions from ~/dotfiles fish (roles/linux-base/files/fish/functions) ----
foreach ($a in 'gc', 'gl', 'ni', 'gp') { if (Test-Path "Alias:$a") { Remove-Item "Alias:$a" -Force } }
function cdd { Set-Location 'C:\work\dotfiles' }
function cdw { Set-Location 'C:\work' }          # projects (= /work in Ubuntu)
# git
function ga { git add . }
function gb { git branch @args }
function gc { git commit -m ($args -join ' ') }
function gco { git checkout @args }
function gf { git flow @args }
function gl { git lg @args }
function gs { git status @args }
function nah { git reset --hard; git clean -df }
function push { git add .; if ($args) { git commit -m ($args -join ' ') } else { git commit -m wip }; git push -u origin HEAD }
# docker compose
function c { docker compose @args }
function up { docker compose up -d --build @args }
function down { docker compose down @args }
function reup { down; up }
function w { docker compose exec --user=laradock workspace bash }
function wex { docker compose exec workspace bash -l -c ($args -join ' ') }
# node / php
function n { npm run @args }
function ni { npm install --save @args }
function pa { php artisan @args }
function reseed { php artisan migrate:fresh --seed }
function sail { & ./vendor/bin/sail @args }
function sa { sail artisan @args }
function phpunit { & ./vendor/bin/phpunit @args }
function p { phpunit }
function pf { & ./vendor/bin/phpunit --filter @args }
# system
function k { Stop-Process -Name ($args -replace '\.exe$', '') -Force }        # killall -9
function rf { Remove-Item -Recurse -Force @args }                             # rm -rf
function fvi { $f = fzf; if ($f) { vim $f } }
function upd { scoop update; scoop update --all; winget upgrade --all --silent --accept-package-agreements --accept-source-agreements }

# prompt and smart cd (z <part of a path>, zi = interactive)
if (Get-Command starship -ErrorAction SilentlyContinue) { Invoke-Expression (& starship init powershell | Out-String) }
if (Get-Command zoxide -ErrorAction SilentlyContinue) { Invoke-Expression (& zoxide init powershell | Out-String) }
