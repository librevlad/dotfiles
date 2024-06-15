#!/bin/bash
sleep 1
rm /tmp/screen.png
scrot /tmp/screen.png
sleep 1
#convert /tmp/screen.png -blur 0x3 /tmp/screen.png
i3lock -i /tmp/screen.png
