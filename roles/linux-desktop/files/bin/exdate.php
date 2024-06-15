<?php

$stdin = `upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep percentage`;

$out = '';

if(preg_match("~[0-9]*%~ims",$stdin,$o))
{ 
   $out .= $o[0] . ' / ';
}

$out .= date('d.m.Y H:i:s');
echo $out;
