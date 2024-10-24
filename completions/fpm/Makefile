all: fpm.yaml
	./generate.sh bash > generated/fpm.bash
	./generate.sh fish > generated/fpm.fish
	./generate.sh zsh  > generated/fpm.zsh

install: fpm.yaml
	./generate.sh bash -i
	./generate.sh fish -i
	./generate.sh zsh -i

fpm.yaml: generate_from_help.py
	./generate_from_help.py > fpm.yaml
