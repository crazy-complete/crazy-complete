generate:
	mkdir -p generated
	mkdir -p generated/bash
	mkdir -p generated/fish
	mkdir -p generated/zsh
	crazy-complete --include-file include.bash bash go-sendxmpp.yaml -o generated/bash/go-sendxmpp
	crazy-complete --include-file include.fish fish go-sendxmpp.yaml -o generated/fish/go-sendxmpp.fish
	crazy-complete --include-file include.zsh  zsh  go-sendxmpp.yaml -o generated/zsh/_go-sendxmpp

install-system-wide:
	crazy-complete --include-file include.bash bash go-sendxmpp.yaml -i
	crazy-complete --include-file include.fish fish go-sendxmpp.yaml -i
	crazy-complete --include-file include.zsh  zsh  go-sendxmpp.yaml -i
