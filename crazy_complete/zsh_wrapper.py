'''Code for generating wrapper.'''

from . import algo
from . import shell
from . import preprocessor

_CODE = r'''
%WRAPPER_FUNC%() {
  %ORIGINAL_COMPLETION_FUNC%

  local i=0 del=0 adjust=0 delete=() new_words=()

  for ((i=1; i <= ${#words[@]}; ++i)); do
    local w="${words[$i]}"

    if false; then
      true
#ifdef long_opts_arg
    elif [[ "$w" == %LONG_OPTS_ARG_PATTERN1% ]]; then
      delete+=($i);
    elif [[ "$w" == %LONG_OPTS_ARG_PATTERN2% ]]; then
      delete+=($i $((++i)));
#endif
#ifdef long_opts_optional
    elif [[ "$w" == %LONG_OPTS_OPTIONAL_PATTERN% ]]; then
      delete+=($i);
#endif
#ifdef long_opts_flag
    elif [[ "$w" == %LONG_OPTS_FLAG_PATTERN% ]]; then
      delete+=($i);
#endif
#ifdef short_opts_arg
    elif [[ "$w" =~ '%SHORT_OPTS_ARG_REGEX1%' ]]; then
      delete+=($i $((++i)));
    elif [[ "$w" =~ '%SHORT_OPTS_ARG_REGEX2%' ]]; then
      delete+=($i);
#endif
#ifdef short_opts_optional
    elif [[ "$w" =~ '%SHORT_OPTS_OPTIONAL_REGEX%' ]]; then
      delete+=($i);
#endif
#ifdef short_opts_flag
    elif [[ "$w" =~ '%SHORT_OPTS_FLAG_REGEX%' ]]; then
      delete+=($i);
#endif
    fi
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


def _make_long_opts_pattern(opts, arg_type):
    if not opts:
        return ''

    long, old = algo.partition(opts, lambda o: o.startswith('--'))

    old = [o.lstrip('-') for o in old]
    long = [o.lstrip('-') for o in long]
    r = ''

    if long and old:
        r = '-(%s|-(%s))' % ('|'.join(old), '|'.join(long))
    elif long:
        r = '--(%s)' % '|'.join(long)
    elif old:
        r = '-(%s)' % '|'.join(old)

    if arg_type == 'arg':
        r += '=*'
    elif arg_type == 'optional':
        r += '(|=*)'

    return r


def _make_short_opts_flag_regex(flag_opts):
    if not flag_opts:
        return ''

    return '^-[%s]+$' % ''.join(flag_opts)


def _make_short_opts_arg_regex(flag_opts, arg_opts, arg_type):
    if not arg_opts:
        return ''

    if flag_opts:
        r = '-[%s]*[%s]' % (''.join(flag_opts), ''.join(arg_opts))
    else:
        r = '-[%s]' % ''.join(arg_opts)

    if arg_type == 'arg':
        r += '.+'
    elif arg_type == 'optional':
        r += '.*'

    return f'^{r}$'


def generate_wrapper(ctxt, commandline):
    completion_funcname = ctxt.helpers.make_completion_funcname(commandline)
    wrapper_funcname = ctxt.helpers.make_completion_funcname(commandline, '__wrapper')

    if not commandline.wraps:
        return (completion_funcname, None)

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

    long_opts_flag_pattern = _make_long_opts_pattern(long_opts_flag, None)
    long_opts_arg_pattern1 = _make_long_opts_pattern(long_opts_arg, 'arg')
    long_opts_arg_pattern2 = _make_long_opts_pattern(long_opts_arg, None)
    long_opts_optional_pattern = _make_long_opts_pattern(long_opts_optional, 'optional')

    short_opts_flag_regex = _make_short_opts_flag_regex(short_opts_flag)
    short_opts_arg_regex1 = _make_short_opts_arg_regex(short_opts_flag, short_opts_arg, None)
    short_opts_arg_regex2 = _make_short_opts_arg_regex(short_opts_flag, short_opts_arg, 'arg')
    short_opts_optional_regex = _make_short_opts_arg_regex(short_opts_flag, short_opts_optional, 'optional')

    s = _CODE.strip()
    s = s.replace('%ORIGINAL_COMPLETION_FUNC%', completion_funcname)
    s = s.replace('%WRAPPER_FUNC%', wrapper_funcname)
    s = s.replace('%WRAPS%', commandline.wraps)
    s = s.replace('%LONG_OPTS_FLAG_PATTERN%', long_opts_flag_pattern)
    s = s.replace('%LONG_OPTS_ARG_PATTERN1%', long_opts_arg_pattern1)
    s = s.replace('%LONG_OPTS_ARG_PATTERN2%', long_opts_arg_pattern2)
    s = s.replace('%LONG_OPTS_OPTIONAL_PATTERN%', long_opts_optional_pattern)
    s = s.replace('%SHORT_OPTS_ARG_REGEX1%', short_opts_arg_regex1)
    s = s.replace('%SHORT_OPTS_ARG_REGEX2%', short_opts_arg_regex2)
    s = s.replace('%SHORT_OPTS_FLAG_REGEX%', short_opts_flag_regex)
    s = s.replace('%SHORT_OPTS_OPTIONAL_REGEX%', short_opts_optional_regex)

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

    s = preprocessor.preprocess(s, defines)

    return (wrapper_funcname, s)
