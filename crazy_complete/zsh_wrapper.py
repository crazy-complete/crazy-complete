'''Code for generating wrapper.'''

from . import cli
from . import algo
from . import preprocessor
from .str_utils import replace_many

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

    long, old = algo.partition(opts, cli.is_long_option_string)

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
    '''Generate code for wrapping a foreign command.'''

    make_completion_funcname = ctxt.helpers.make_completion_funcname
    completion_funcname = make_completion_funcname(commandline)
    wrapper_funcname = make_completion_funcname(commandline, '__wrapper')

    if not commandline.wraps:
        return (completion_funcname, None)

    long_opts_arg = []
    long_opts_flag = []
    long_opts_optional = []

    short_opts_arg = []
    short_opts_flag = []
    short_opts_optional = []

    for option in commandline.get_options():
        if option.has_required_arg():
            long_opts_arg += option.get_long_option_strings()
            long_opts_arg += option.get_old_option_strings()
            short_opts_arg += option.get_short_option_strings()
        elif option.has_optional_arg():
            long_opts_optional += option.get_long_option_strings()
            long_opts_optional += option.get_old_option_strings()
            short_opts_optional += option.get_short_option_strings()
        else:
            long_opts_flag += option.get_long_option_strings()
            long_opts_flag += option.get_old_option_strings()
            short_opts_flag += option.get_short_option_strings()

    short_opts_flag = ''.join(o[1] for o in short_opts_flag)

    s = _CODE.strip()
    s = replace_many(s, [
        ('%ORIGINAL_COMPLETION_FUNC%',
         completion_funcname),

        ('%WRAPPER_FUNC%',
         wrapper_funcname),

        ('%WRAPS%',
         commandline.wraps),

        ('%LONG_OPTS_FLAG_PATTERN%',
         _make_long_opts_pattern(long_opts_flag, None)),

        ('%LONG_OPTS_ARG_PATTERN1%',
         _make_long_opts_pattern(long_opts_arg, 'arg')),

        ('%LONG_OPTS_ARG_PATTERN2%',
         _make_long_opts_pattern(long_opts_arg, None)),

        ('%LONG_OPTS_OPTIONAL_PATTERN%',
         _make_long_opts_pattern(long_opts_optional, 'optional')),

        ('%SHORT_OPTS_FLAG_REGEX%',
         _make_short_opts_flag_regex(short_opts_flag)),

        ('%SHORT_OPTS_ARG_REGEX1%',
         _make_short_opts_arg_regex(short_opts_flag, short_opts_arg, None)),

        ('%SHORT_OPTS_ARG_REGEX2%',
         _make_short_opts_arg_regex(short_opts_flag, short_opts_arg, 'arg')),

        ('%SHORT_OPTS_OPTIONAL_REGEX%',
         _make_short_opts_arg_regex(short_opts_flag, short_opts_optional, 'optional'))
    ])

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
