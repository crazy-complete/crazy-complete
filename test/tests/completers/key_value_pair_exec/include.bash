_complete_key_value_pair() {
  if (( $# == 0 )); then
    printf '%s\t%s\n'                \
      'async'     'set async mode'   \
      'animal='   'select an animal' \
      'special'   "special chars: []'\"\$\`\\"
  else
    case "$1" in
      animal)
        printf '%s\t%s\n'     \
          'cat'     'a cat'   \
          'dog'     'a dog'   \
          'horse'   'a horse' \
          'special' ":[]'\"\$\`\\";;
      esac
  fi
}
