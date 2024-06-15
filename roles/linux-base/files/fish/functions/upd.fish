# Defined in /tmp/fish.Eh3ddA/upd.fish @ line 1
function upd
    sudo apt update
    sudo apt full-upgrade
    sudo apt autoremove
    sudo apt autoclean
    sudo apt clean
    purge-old-kernels
    sudo snap refresh
end
