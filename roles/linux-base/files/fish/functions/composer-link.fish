# Defined in /tmp/fish.inUDYY/composer-link.fish @ line 2
function composer-link
	composer config repositories.local-$argv '{"type": "path", "url": "'$argv'"}' --file composer.json
end
