_complete_key_value_list() {
  if (( $# == 0 )); then
    printf '%s\t%s\t%s\n'                                       \
      'async'       'set async mode'             ''             \
      'animal='     'select an animal'           ''             \
      'optional=?'  'optional argument'          ''             \
      'special'     "special chars: []'\"\$\`\\" ''             \
      'exclusive'   'disable options'            'async animal' \
      '*repeatable' 'repeatable option'          ''
  else
    case "$1" in
      animal|optional)
        printf '%s\t%s\n'     \
          'cat'     'a cat'   \
          'dog'     'a dog'   \
          'horse'   'a horse' \
          'special' ":[]'\"\$\`\\";;
      esac
  fi
}
