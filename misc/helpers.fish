#!/bin/fish

function __fish_helper
  # ===========================================================================
  #
  # This function implements the parsing of options and positionals in the Fish shell.
  #
  # Usage: __fish_helper <OPTIONS> <COMMAND> [ARGS...]
  #
  # The first argument is a comma-seperated list of options that the parser should know about.
  # Short options (-o), long options (--option), and old-style options (-option) are supported.
  #
  # If an option takes an argument, it is suffixed by '='.
  # If an option takes an optional argument, it is suffixed by '=?'.
  #
  # For example:
  #   __fish_helper '-f,--flag,-old-style,--with-arg=,--with-optional=?'
  #
  #   Here, -f, --flag and -old-style don't take options, --with-arg requires an
  #   argument and --with-optional takes an optional argument.
  #
  # COMMANDS
  #   positional_contains <NUM> <WORDS...>
  #     Checks if the positional argument number NUM is one of WORDS.
  #     NUM counts from one.
  #
  #   has_option <OPTIONS...>
  #     Checks if a option given in OPTIONS is passed on commandline.
  #
  #   option_is <OPTIONS...> -- <VALUES...>
  #     Checks if any option in OPTIONS has a value of VALUES.
  #
  #   num_of_positionals [<OPERATOR> <NUMBER>]
  #     Checks the number of positional arguments.
  #     If no arguments are provided, print the total count of positional arguments.
  #     If two arguments are provided, the first argument should be one of
  #     the comparison operators: '-lt', '-le', '-eq', '-ne', '-gt', '-ge'.
  #     Returns 0 if the count of positional arguments matches the
  #     specified NUMBER according to the comparison operator, otherwise returns 1.
  #
  # ===========================================================================

  set -l func '__fish_helper'

  set -l positionals
  set -l having_options
  set -l option_values

#if DEBUG
  switch (count $argv)
    case 0
      echo "$func: missing OPTIONS argument" >&2
      return 1
    case 1
      echo "$func: missing COMMAND" >&2
      return 1
  end
#endif

  set -l options $argv[1]
  set -e argv[1]

  set -l cmd $argv[1]
  set -e argv[1]

  set -l my_cache_key "$(commandline -b) $options"

  if test "$__CACHE_KEY" = "$my_cache_key"
    set positionals    $__CACHE_POSITIONALS
    set having_options $__CACHE_HAVING_OPTIONS
    set option_values  $__CACHE_OPTION_VALUES
  else
    # =========================================================================
    # Parsing of OPTIONS argument
    # =========================================================================

    set -l short_opts_with_arg
    set -l long_opts_with_arg
    set -l old_opts_with_arg

    set -l short_opts_without_arg
    set -l long_opts_without_arg
    set -l old_opts_without_arg

    set -l short_opts_with_optional_arg
    set -l long_opts_with_optional_arg
    set -l old_opts_with_optional_arg

    set -l option

    if test -n "$options"
      for option in (string split -- ',' $options)
        # Using one big switch case is the fastest way
        switch $option
          case '--?*=';   set -a long_opts_with_arg           (string replace -- '='  '' $option)
          case '--?*=\?'; set -a long_opts_with_optional_arg  (string replace -- '=?' '' $option)
          case '--?*';    set -a long_opts_without_arg        $option

          case '-?=';     set -a short_opts_with_arg          (string replace -- '='  '' $option)
          case '-?=\?';   set -a short_opts_with_optional_arg (string replace -- '=?' '' $option)
          case '-?';      set -a short_opts_with_arg          $option

          case '-??*=';   set -a old_opts_with_arg            (string replace -- '='  '' $option)
          case '-??*=\?'; set -a old_opts_with_optional_arg   (string replace -- '=?' '' $option)
          case '-??*';    set -a old_opts_without_arg         $option

          case '*'
            echo "$func: argv[1]: '$option' is not a short, long or old-style option" >&2
            return 1
        end
      end
    end

    # =========================================================================
    # Parsing of options and positionals
    # =========================================================================

    set -l cmdline (commandline -poc)
    set -l cmdline_count (count $cmdline)

    set -l argi 2 # cmdline[1] is command name
    while test $argi -le $cmdline_count
      set -l arg "$cmdline[$argi]"
      set -l have_trailing_arg (test $argi -lt $cmdline_count && echo true || echo false)

      switch $arg
        case '-'
          set -a positionals -
        case '--'
          for argi in (seq (math $argi + 1) $cmdline_count)
            set -a positionals $cmdline[$argi]
          end
          break
        case '--*'
          for option in $long_opts_with_arg $long_opts_without_arg $long_opts_with_optional_arg
            if string match -q -- "$option=*" $arg
              set -a having_options $option
              set -a option_values (string replace -- "$option=" "" $arg)
              break
            else if string match -q -- $option $arg
              if contains -- $option $long_opts_with_arg
                if $have_trailing_arg
                  set -a having_options $option
                  set -a option_values $cmdline[(math $argi + 1)]
                  set argi (math $argi + 1)
                end
              else
                set -a having_options $option
                set -a option_values ""
              end
              break
            end
          end
        case '-*'
          set -l have_match false

          for option in $old_opts_with_arg $old_opts_without_arg $old_opts_with_optional_arg
            if string match -q -- "$option=*" $arg
              set -a having_options $option
              set -a option_values (string replace -- "$option=" "" $arg)
              set have_match true
              break
            else if string match -q -- $option $arg
              if contains -- $option $old_opts_with_arg
                if $have_trailing_arg
                  set -a having_options $option
                  set -a option_values $cmdline[(math $argi + 1)]
                  set argi (math $argi + 1)
                end
              else
                set -a having_options $option
                set -a option_values ""
              end

              set have_match true
              break
            end
          end

          if not $have_match
            set -l arg_length (string length -- $arg)
            set -l i 2
            set is_end false
            while not $is_end && test $i -le $arg_length
              set -l char (string sub -s $i -l 1 -- "$arg")
              set -l have_trailing_chars (test $i -lt $arg_length && echo true || echo false)

              for option in $short_opts_with_arg $short_opts_without_arg $short_opts_with_optional_arg
                set -l option_char (string sub -s 2 -l 1 -- $option)

                if test "$char" = "$option_char"
                  if contains -- $option $short_opts_with_arg
                    if $have_trailing_chars
                      set -a having_options $option
                      set -a option_values (string sub -s (math $i + 1) -- $arg)
                      set is_end true
                    else if $have_trailing_arg
                      set -a having_options $option
                      set -a option_values $cmdline[(math $argi + 1)]
                      set argi (math $argi + 1)
                      set is_end true
                    end
                  else if contains -- $option $short_opts_with_optional_arg
                    set -a having_options $option

                    if $have_trailing_chars
                      set -a option_values (string sub -s (math $i + 1) -- $arg)
                      set is_end true
                    else
                      set -a option_values ""
                    end
                  else
                    set -a having_options $option
                    set -a option_values ""
                  end

                  break
                end
              end

              set i (math $i + 1)
            end
          end
        case '*'
          set -a positionals $arg
      end

      set argi (math $argi + 1)
    end

    set -g __CACHE_POSITIONALS    $positionals
    set -g __CACHE_HAVING_OPTIONS $having_options
    set -g __CACHE_OPTION_VALUES  $option_values
    set -g __CACHE_KEY            $my_cache_key
  end

  # ===========================================================================
  # Commands
  # ===========================================================================

  switch $cmd
#if POSITIONAL_CONTAINS
    case 'positional_contains'
      if test (count $argv) -eq 0
        echo "$func: positional_contains: argv[3]: missing number" >&2
        return 1
      end

      set -l positional_num $argv[1]
      set -e argv[1]
      contains -- $positionals[$positional_num] $argv && return 0 || return 1
#endif
#if HAS_OPTION
    case 'has_option'
      for option in $having_options
        contains -- $option $argv && return 0
      end

      return 1
#endif
#if NUM_OF_POSITIONALS
    case 'num_of_positionals'
      switch (count $argv)
        case 0
          count $positionals
        case 1
          echo "$func: num_of_positionals: $argv[1]: missing operand" >&2
          return 1
        case 2
          if contains -- $argv[1] -lt -le -eq -ne -gt -ge;
            test (count $positionals) $argv[1] $argv[2] && return 0 || return 1
          else
            echo "$func: num_of_positionals: $argv[1]: unknown operator" >&2
            return 1
          end
        case '*'
          echo "$func: num_of_positionals: too many arguments" >&2
          return 1
      end
#endif
#if OPTION_IS
    case 'option_is'
      set -l options
      set -l values

      for arg in $argv
        set -e argv[1]

        if string match -q -- -- $arg
          set values $argv
          break
        else
          set -a options $arg
        end
      end

      if test (count $values) -eq 0
        echo "$func: missing values" >&2
        return 1
      end

      set -l i (count $having_options)
      while test $i -ge 1
        if contains -- $having_options[$i] $options
          if contains -- $option_values[$i] $values
            return 0
          end
        end

        set i (math $i - 1)
      end

      return 1
#endif
#if DEBUG
    case '*'
      echo "$func: argv[2]: invalid command" >&2
      return 1
#endif
  end
end

function __fish_complete_filedir -d "Complete files or directories"
  # Function for completing files or directories
  #
  # Options:
  #   -d|--description=DESC   The description for completed entries
  #   -c|--comp=STR           Complete STR instead of current command line argument
  #   -D|--directories        Only complete directories
  #   -C|--cd=DIR             List contents in DIR
  #
  # This function is made out of /usr/share/fish/functions/__fish_complete_directories.fish

  argparse --max-args 0 'd/description=' 'c/comp=' 'D/directories' 'C/cd=' -- $argv || return 1

  set -l comp
  set -l desc

  if set -q _flag_description[1]
    set desc $_flag_description
  else if set -g _flag_directories
    set desc 'Directory'
  end

  if set -q _flag_comp[1]
    set comp $_flag_comp
  else
    set comp (commandline -ct | string replace -r -- '^-[^=]*=' '')
  end

  if set -q _flag_cd[1]
    pushd $_flag_cd || return 1
  end

  set -l files (complete -C"'' $comp")

  if set -q _flag_cd[1]
    popd
  end

  if set -q files[1]
    if set -q _flag_directories[1]
      set files (printf "%s\n" $files | string match -r '.*/$')
    end

    printf "%s\n" $files\t"$desc"
  end
end

function simple_values
  set -l SEPARATOR $argv[1]
  set -e argv[1]
  set -l VALUES $argv

  set -l cmdline (commandline -po)
  set -l cur $cmdline[(count $cmdline)]

  set -S cmdline cur >> /tmp/trace

  set -l VALUE
  set -l c (commandline -b)

  if test (string sub -s -1 -l 1 -- $c) = ' '
    for VALUE in $VALUES
      printf "%s\n" $VALUE
    end
    return
  end

  set -l HAVING_VALUES (string split -- $SEPARATOR $cur)
  set -l REMAINING_VALUES
  set -l HAVING_VALUE

  for VALUE in $VALUES
    set -l FOUND_VALUE false

    for HAVING_VALUE in $HAVING_VALUES
      echo "test '$VALUE' = '$HAVING_VALUE'" >> /tmp/trace
      if test $VALUE = $HAVING_VALUE
        set FOUND_VALUE true
        break
      end
    end

    if ! $FOUND_VALUE
      set -a REMAINING_VALUES $VALUE
    end
  end

  if string match -q -r -- $SEPARATOR'$' $cur # TODO
    for VALUE in $REMAINING_VALUES
      printf "%s%s\n" $cur $VALUE
    end
  else if test (count $HAVING_VALUES) -gt 0
    set CUR_LAST_VALUE $HAVING_VALUES[-1]

    for VALUE in $REMAINING_VALUES
      if string match -q -- $CUR_LAST_VALUE'*' $VALUE
        printf "%s\n" $VALUE
      end
    end
  end
end

# =============================================================================
# Test code
# =============================================================================

set -l options "--arg=,-a=,-oldarg=,-optional=?,--flag,-f,-flag"

complete -c foo -e
complete -c foo -n "__fish_helper '$options' num_of_positionals -eq 0" -x -a 'first'
complete -c foo -n "__fish_helper '$options' positional_contains 1 first && not __fish_helper '$options' has_option -a --arg -oldarg" -f -s a -l arg -o oldarg -r -a '1 2 3'
complete -c foo -n "__fish_helper '$options' positional_contains 1 first && not __fish_helper '$options' has_option -optional" -f -o optional -a '1 2 3'

complete -c foo -l files      -x -a '(__fish_complete_filedir)'
complete -c foo -l dirs       -x -a '(__fish_complete_filedir -D)'
complete -c foo -l temp-files -x -a '(__fish_complete_filedir -C /tmp)'
complete -c foo -l temp-dirs  -x -a '(__fish_complete_filedir -D -C /tmp)'
complete -c foo -l desc-files -x -a '(__fish_complete_filedir -d Foo)'

complete -c foo -l simple-values -x -a '(simple_values , foo bar baz)'
