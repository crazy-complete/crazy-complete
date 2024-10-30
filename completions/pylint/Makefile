pylint.yaml: update_yaml.py
	pylint -h > pylint.help.txt
	crazy-complete --input-type=help yaml pylint.help.txt > pylint.from_help.yaml
	./update_yaml.py pylint.from_help.yaml > pylint.yaml

generate_completions:
	mkdir -p generated
	crazy-complete bash pylint.yaml -o generated/pylint.bash
	crazy-complete --repeatable-options=True fish pylint.yaml -o generated/pylint.fish
	crazy-complete zsh  pylint.yaml -o generated/pylint.zsh

install_completions:
	crazy-complete -i bash pylint.yaml
	crazy-complete -i --repeatable-options=True fish pylint.yaml
	crazy-complete -i zsh  pylint.yaml
