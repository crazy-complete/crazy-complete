CRAZY_COMPLETE ?= ../crazy-complete

all: bash fish zsh

bash:
	mkdir -p generated/bash
	
	$(CRAZY_COMPLETE) \
		--inherit-options=True \
		-o generated/bash/example \
		bash example.yaml

fish:
	mkdir -p generated/fish
	
	$(CRAZY_COMPLETE) \
		--inherit-options=True \
		-o generated/fish/example.fish \
		fish example.yaml 

zsh:
	mkdir -p generated/zsh
	
	$(CRAZY_COMPLETE) \
		--inherit-options=True \
		-o generated/zsh/_example \
		zsh example.yaml 
	
	$(CRAZY_COMPLETE) \
		--inherit-options=True \
		--zsh-compdef=False \
		-o generated/zsh/example.sourceable \
		zsh example.yaml

clean:
	rm -rf generated
