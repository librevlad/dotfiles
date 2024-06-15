function become
	rm -rf ~/.ssh/id_rsa*; ln -s ~/.ssh/$argv/id_rsa ~/.ssh/id_rsa; ln -s ~/.ssh/$argv/id_rsa.pub ~/.ssh/id_rsa.pub
end
