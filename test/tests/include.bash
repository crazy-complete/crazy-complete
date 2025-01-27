_complete_internal() {
  COMPREPLY=( $(compgen -W 'one two three') )
}
