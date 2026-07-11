function _complete_key_value_pair
  if test (count $argv) -eq 0
    printf '%s\t%s\n'                \
      'async'     'set async mode'   \
      'animal='   'select an animal' \
      'special'   "special chars: []'\"\$`\\"
  else
    switch "$argv[1]"
      case animal
        printf '%s\t%s\n'     \
          'cat'     'a cat'   \
          'dog'     'a dog'   \
          'horse'   'a horse' \
          'special' ":[]'\"\$`\\"
    end
  end
end
