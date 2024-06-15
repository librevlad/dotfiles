# Defined in - @ line 2
function fixmedia
	sudo umount /dev/sda1
    sudo ntfsfix /dev/sda1
    sudo mount -t ntfs-3g /dev/sda1 /mnt/media
end
