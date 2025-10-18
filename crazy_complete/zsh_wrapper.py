'''Code for generating wrapper.'''

from . import shell
from . import preprocessor

_CODE = r'''
%WRAPPER_FUNC%() {
  %ORIGINAL_COMPLETION_FUNC%

  local i=0 del=0 adjust=0 delete=() new_words=() opt=''
#ifdef long_opts_arg
  local long_opts_arg=(%LONG_OPTS_WITH_ARG%)
#endif
#ifdef long_opts_flag
  local long_opts_flag=(%LONG_OPTS_FLAG%)
#endif
#ifdef long_opts_optional
  local long_opts_optional=(%LONG_OPTS_OPTIONAL%)
#endif
#ifdef short_opts_arg
  local short_opts_arg=(%SHORT_OPTS_WITH_ARG%)
#endif
#ifdef short_opts_flag
  local short_opts_flag=(%SHORT_OPTS_FLAG%)
#endif
#ifdef short_opts_optional
  local short_opts_optional=(%SHORT_OPTS_OPTIONAL%)
#endif

  for ((i=1; i <= ${#words[@]}; ++i)); do
    local word="${words[$i]}"
#ifdef long_opts_arg

    for opt in "${long_opts_arg[@]}"; do
      if [[ "$word" == "$opt"* ]]; then
        delete+=($i);
        continue 2;
      elif [[ "$word" == "$opt" ]]; then
        delete+=($i $((++i)));
        continue 2;
      fi
    done
#endif
#ifdef long_opts_optional

    for opt in "${long_opts_optional[@]}"; do
      if [[ "$word" == "$opt"* ]]; then
        delete+=($i);
        continue 2;
      fi
    done
#endif
#ifdef long_opts_flag

    for opt in "${long_opts_flag[@]}"; do
      if [[ "$word" == "$opt" ]]; then
        delete+=($i);
        continue 2;
      fi
    done
#endif
#ifdef short_opts_any

    [[ "$word" == --* ]] && continue
#endif
#ifdef short_opts_arg

    for opt in "${short_opts_arg[@]}"; do
      if [[ "$word" == '-'*"$opt" ]]; then
        delete+=($i $((++i)));
        continue 2;
      elif [[ "$word" == '-'*"$opt"* ]]; then
        delete+=($i);
        continue 2;
      fi
    done
#endif
#ifdef short_opts_optional

    for opt in "${short_opts_optional[@]}"; do
      if [[ "$word" == '-'*"$opt"* ]]; then
        delete+=($i);
        continue 2;
      fi
    done
#endif
#ifdef short_opts_flag

    for opt in "${short_opts_flag[@]}"; do
      if [[ "$word" == '-'*"$opt"* ]]; then
        delete+=($i);
        continue 2;
      fi
    done
#endif
  done

  for del in "${delete[@]}"; do
    (( del < CURRENT )) && (( ++adjust ))
  done

  (( CURRENT -= adjust ))

  for ((i=1; i <= ${#words[@]}; ++i)); do
    if [[ " ${delete[@]} " != *" $i "* ]]; then
      new_words+=("${words[$i]}")
    fi
  done

  words=("${new_words[@]}")
  words[1]='%WRAPS%'

  service=%WRAPS%
  (( $+_comps[%WRAPS%] )) && $_comps[%WRAPS%]
}
'''

def generate_wrapper(generators):
    first_generator = generators[0]
    commandline = first_generator.commandline

    if not commandline.wraps:
        return (shell.make_completion_funcname(commandline), None)

    completion_funcname = shell.make_completion_funcname(commandline)
    wrapper_funcname = '%s__wrapper' % completion_funcname

    long_opts_arg = []
    long_opts_flag = []
    long_opts_optional = []

    short_opts_arg = []
    short_opts_flag = []
    short_opts_optional = []

    for option in commandline.get_options():
        if option.complete and option.optional_arg is False:
            long_opts_arg.extend(option.get_long_option_strings())
            long_opts_arg.extend(option.get_old_option_strings())
            short_opts_arg.extend(o.lstrip('-') for o in option.get_short_option_strings())
        elif option.complete:
            long_opts_optional.extend(option.get_long_option_strings())
            long_opts_optional.extend(option.get_old_option_strings())
            short_opts_optional.extend(o.lstrip('-') for o in option.get_short_option_strings())
        else:
            long_opts_flag.extend(option.get_long_option_strings())
            long_opts_flag.extend(option.get_old_option_strings())
            short_opts_flag.extend(o.lstrip('-') for o in option.get_short_option_strings())

    s = _CODE
    s = s.replace('%ORIGINAL_COMPLETION_FUNC%', completion_funcname)
    s = s.replace('%WRAPPER_FUNC%', wrapper_funcname)
    s = s.replace('%WRAPS%', commandline.wraps)
    s = s.replace('%LONG_OPTS_FLAG%', ' '.join(long_opts_flag))
    s = s.replace('%LONG_OPTS_WITH_ARG%', ' '.join(long_opts_arg))
    s = s.replace('%LONG_OPTS_OPTIONAL%', ' '.join(long_opts_optional))
    s = s.replace('%SHORT_OPTS_FLAG%', ' '.join(short_opts_flag))
    s = s.replace('%SHORT_OPTS_WITH_ARG%', ' '.join(short_opts_arg))
    s = s.replace('%SHORT_OPTS_OPTIONAL%', ' '.join(short_opts_optional))

    defines = []
    if long_opts_flag:
        defines.append('long_opts_flag')
    if long_opts_arg:
        defines.append('long_opts_arg')
    if long_opts_optional:
        defines.append('long_opts_optional')
    if short_opts_flag:
        defines.append('short_opts_flag')
    if short_opts_arg:
        defines.append('short_opts_arg')
    if short_opts_optional:
        defines.append('short_opts_optional')
    if short_opts_flag or short_opts_arg or short_opts_optional:
        defines.append('short_opts_any')

    s = preprocessor.preprocess(s, defines)

    return (wrapper_funcname, s)
