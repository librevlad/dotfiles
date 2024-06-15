function ch
	if count $argv >/dev/null
        sudo chmod -R 777 $argv
    else
        sudo chmod -R 777 ./
    end
end
