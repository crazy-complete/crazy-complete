_amixer_list_simple_mixer_control() {
  amixer scontrols | sed 's/Simple mixer control //' | tr -d "'"
}

_amixer_list_mixer_control() {
  amixer controls | tr -d "'"
}
