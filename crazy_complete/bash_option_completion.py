'''Module for option completion in Bash.'''

from . import algo
from . import utils
from . import bash_when
from . import bash_utils
from .str_utils import indent

class MasterCompletionFunction:
    '''Class for generating a master completion function.'''

    def __init__(self, options, abbreviations, complete, generator):
        self.abbreviations = abbreviations
        self.complete = complete
        self.generator = generator
        self.code = []

        optional_arg = list(filter(lambda o: o.complete and o.optional_arg is True, options))
        required_arg = list(filter(lambda o: o.complete and o.optional_arg is False, options))

        self._add_options(required_arg)

        if optional_arg:
            self.code.append('[[ "$mode" == WITH_OPTIONAL ]] || return 1')
            self._add_options(optional_arg)

    def _get_all_option_strings(self, option):
        opts = []
        opts.extend(self.abbreviations.get_many_abbreviations(option.get_long_option_strings()))
        opts.extend(self.abbreviations.get_many_abbreviations(option.get_old_option_strings()))
        opts.extend(option.get_short_option_strings())
        return opts

    def _add_options(self, options):
        with_when, without_when = algo.partition(options, lambda o: o.when)
        self._add_options_with_when(with_when)
        self._add_options_without_when(without_when)

    def _add_options_without_when(self, options):
        options_group_by_complete = algo.group_by(options, lambda o: self.complete(o, False))

        if options_group_by_complete:
            r = 'case "$opt" in\n'
            for complete, options in options_group_by_complete.items():
                opts = algo.flatten([self._get_all_option_strings(o) for o in options])
                r += '  %s)\n' % '|'.join(opts)
                if complete:
                    r += '%s\n' % indent(complete, 4)
                r += '    return 0;;\n'
            r += 'esac'
            self.code.append(r)

    def _add_options_with_when(self, options):
        for option in options:
            opts = self._get_all_option_strings(option)
            completion_code = self.complete(option, False)
            cond = bash_when.generate_when_conditions(
                self.generator.commandline,
                self.generator.variable_manager,
                option.when)

            r  = 'case "$opt" in %s)\n' % '|'.join(opts)
            r += '  if %s; then\n' % cond
            if completion_code:
                r += '%s\n' % indent(completion_code, 4)
            r += '    return 0\n'
            r += '  fi;;\n'
            r += 'esac'
            self.code.append(r)

    def get(self, funcname):
        '''Get the function code.'''

        if self.code:
            r  = '%s() {\n' % funcname
            r += '  local opt="$1" cur="$2" mode="$3"\n\n'
            r += '%s\n\n' % indent('\n\n'.join(self.code), 2)
            r += '  return 1\n'
            r += '}'
            return r

        return None

def generate_option_completion(self):
    r = ''
    options = self.commandline.get_options(only_with_arguments=True)

    if self.commandline.abbreviate_options:
        # If we inherit options from parent commands, add those
        # to the abbreviation generator
        abbreviations = bash_utils.get_OptionAbbreviationGenerator(
            self.commandline.get_options(
                with_parent_options=self.commandline.inherit_options))
    else:
        abbreviations = utils.DummyAbbreviationGenerator()

    complete_option = MasterCompletionFunction(
        options, abbreviations, self._complete_option, self)
    code = complete_option.get('__complete_option')

    if not code:
        return None

    r += '%s\n\n' % code

    # pylint: disable=invalid-name
    LR = False # Long with required argument
    LO = False # Long with optional argument
    SR = False # Short with required argument
    SO = False # Short with optional argument
    OR = False # Old-Style with required argument
    OO = False # Old-Style with optional argument

    for option in options:
        if option.get_long_option_strings():
            if option.complete and option.optional_arg is True:
                LO = True
            elif option.complete:
                LR = True

        if option.get_old_option_strings():
            if option.complete and option.optional_arg is True:
                OO = True
            elif option.complete:
                OR = True

        if option.get_short_option_strings():
            if option.complete and option.optional_arg is True:
                SO = True
            elif option.complete:
                SR = True

    G0 = LR or OR or SR
    G1 = LR or LO or OR or OO or SR or SO
    G2 = SR or SO

    prefix_compreply_func = ''
    if G2:
        prefix_compreply_func = self.ctxt.helpers.use_function('prefix_compreply')

    is_oldstyle_option = None
    if G2:
        all_options = algo.flatten(abbreviations.get_many_abbreviations(
            o.get_old_option_strings()) for o in self.commandline.get_options(with_parent_options=True))
        if all_options:
            is_oldstyle_option = '''\
__is_oldstyle_option() {
case "$1" in %s) return 0;; esac
return 1
}\n\n''' % '|'.join(all_options)
            r += is_oldstyle_option

    OLD = is_oldstyle_option

    short_no_args = ''
    short_required_args = ''
    for option in self.commandline.get_options(with_parent_options=True):
        if option.complete and option.optional_arg is False:
            short_required_args += ''.join(o.lstrip('-') for o in option.get_short_option_strings())
        elif option.complete is None:
            short_no_args += ''.join(o.lstrip('-') for o in option.get_short_option_strings())

    short_no_args_pattern = ''
    if short_no_args:
        short_no_args_pattern = '*([%s])' % short_no_args

    code = [
      # CONDITION, TEXT
      (G0        , 'case "$prev" in\n'),
      (G0        , '  --*)'),
      (LR        , '\n    __complete_option "$prev" "$cur" WITHOUT_OPTIONAL && return 0'),
      (G0        , ';;\n'),
      (G0        , '  -*)'),
      (OR        , '\n    __complete_option "$prev" "$cur" WITHOUT_OPTIONAL && return 0'),
      (SR        , '\n    case "$prev" in -%s[%s])' % (short_no_args_pattern, short_required_args)),
      (SR        , '\n      __complete_option "-${prev: -1}" "$cur" WITHOUT_OPTIONAL && return 0'),
      (SR        , '\n    esac'),
      (G0        , ';;\n'),
      (G0        , 'esac\n'),
      (G0        , '\n'),

      (G1        , 'case "$cur" in\n'),
      (G1        , '  --*=*)'),
      (LR|LO     , '\n    __complete_option "${cur%%=*}" "${cur#*=}" WITH_OPTIONAL && return 0'),
      (G1        , ';;\n'),
      (G1        , '  -*=*)'),
      (OR|OO     , '\n    __complete_option "${cur%%=*}" "${cur#*=}" WITH_OPTIONAL && return 0'),
      (G1        , ';;\n'),
      (G1        , '  --*);;\n'),
      (G1        , '  -*)'),
      (G2 and OLD, '\n    if ! __is_oldstyle_option "$cur"; then'),
      (G2        , '\n      local i'),
      (G2        , '\n      for ((i=2; i <= ${#cur}; ++i)); do'),
      (G2        , '\n        local pre="${cur:0:$i}" value="${cur:$i}"'),
      (SR|SO     , '\n        __complete_option "-${pre: -1}" "$value" WITH_OPTIONAL && {'),
      (SR|SO     , '\n          %s "$pre"' % prefix_compreply_func),
      (SR|SO     , '\n          return 0'),
      (SR|SO     , '\n        }'),
      (G2        , '\n      done'),
      (G2 and OLD, '\n    fi'),
      (G1        , ';;\n'),
      (G1        , 'esac')
    ]

    r += ''.join(c[1] for c in code if c[0])

    return r.strip()
