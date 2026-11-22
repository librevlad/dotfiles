#Requires AutoHotkey v2.0
#SingleInstance Force
#NoTrayIcon
; GlazeWM swallows the key of its Win+key bindings, so Windows sees a lone Win press and opens Start when Win goes
; up (glzr-io/glazewm#1215; worst for bindings that start a program: Win+Enter, Win+`). A dummy key (vkE8 is not
; assigned to anything) sent the moment Win goes down tells Windows "Win was used with another key", so Win never
; opens Start. Start: Ctrl+Esc; apps: Win+S (Flow Launcher). Started from shell:startup (no-start-menu.lnk).
~LWin::Send "{Blind}{vkE8}"
~RWin::Send "{Blind}{vkE8}"
