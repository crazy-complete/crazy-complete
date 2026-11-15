# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 Benjamin Abendroth <braph93@gmx.de>

'''Wraps the generated Bash completion function with a finalizing entry point.'''

from .helpers import ShellFunction, replace_function_name


_FINALIZE = r'''
%FUNCNAME%() {
  local _CC_CUR _CC_CUR_PREFIX_OPTION
  local word word_dequoted breakpos=-1 in_quote=0 word_prefix='' value
  local -a out=()

  %INNER_FUNCNAME% "$@"
  local rc=$?

  word="$_CC_CUR"

  if (( ${#_CC_CUR_PREFIX_OPTION} == 2 )); then
    word="${word#-*${_CC_CUR_PREFIX_OPTION:1:1}}"
  elif (( ${#_CC_CUR_PREFIX_OPTION} > 0 )); then
    word="${word#"$_CC_CUR_PREFIX_OPTION"=}"
  fi

  dequote "$word" word_dequoted breakpos in_quote

  if (( breakpos != -1 )); then
    word_prefix="${word_dequoted:0:breakpos}"
  fi

  for value in "${COMPREPLY[@]}"; do
    if (( breakpos != -1 )) && [[ "$value" == "$word_prefix"* ]]; then
      value="${value:$breakpos}"
    fi

    if [[ "$value" == *[!A-Za-z0-9_:,/+-]* ]]; then
      case "$in_quote" in
        0) value="$(printf '%q' "$value")"
           value="${value//'\,'/,}";;
        1) value="$(sq_quote "$value")";;
        2) value="$(dq_quote "$value")";;
      esac
    fi

    out+=("$value")
  done

  COMPREPLY=("${out[@]}")
  return $rc
}
'''


def generate_finalizer(ctxt, commandline, inner_funcname):
    '''Finalize-wrapper: runs the completion function, then finalizes.'''

    funcname = ctxt.helpers.make_completion_funcname(commandline, '__finalize')

    r = _FINALIZE
    r = r.replace('%FUNCNAME%', funcname)
    r = r.replace('%INNER_FUNCNAME%', inner_funcname)
    r = replace_function_name('dequote', ctxt.helpers.use_function('dequote'), r)
    r = replace_function_name('sq_quote', ctxt.helpers.use_function('sq_quote'), r)
    r = replace_function_name('dq_quote', ctxt.helpers.use_function('dq_quote'), r)

    return (funcname, r)
