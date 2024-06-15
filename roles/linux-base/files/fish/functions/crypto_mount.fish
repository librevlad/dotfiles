function crypto_mount
	sudo mount -t ecryptfs $argv -o ecryptfs_cipher=aes,ecryptfs_key_bytes=32,key=passphrase,ecryptfs_passthrough=n,ecryptfs_enable_filename_crypto=y
end
