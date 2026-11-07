function _complete_key_value_list
  if test (count $argv) -eq 0
    printf '%s\t%s\t%s\n'                                      \
      'async'       'set async mode'            ''             \
      'animal='     'select an animal'          ''             \
      'optional=?'  'optional argument'         ''             \
      'special'     "special chars: []'\"\$`\\" ''             \
      'exclusive'   'disable options'           'async animal' \
      '*repeatable' 'repeatable option'         ''
  else
    switch "$argv[1]"
      case animal optional
        printf '%s\t%s\n'     \
          'cat'     'a cat'   \
          'dog'     'a dog'   \
          'horse'   'a horse' \
          'special' ":[]'\"\$`\\"
    end
  end
end
