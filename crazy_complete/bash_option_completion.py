from collections import OrderedDict

from . import algo
from . import utils
from . import bash_when

class MasterCompletionFunction:
    def __init__(self, name, options, abbreviations, complete, generator):
        self.name = name
        self.options = options
        self.abbreviations = abbreviations
        self.complete = complete
        self.generator = generator
        self.code = []

        options_with_optional_arg = []
        options_with_required_arg = []

        for option in options:
            if option.complete and option.optional_arg is True:
                options_with_optional_arg.append(option)
            elif option.complete:
                options_with_required_arg.append(option)

        self.add_options(options_with_required_arg)
        if options_with_optional_arg:
            self.code.append('[[ "$mode" == WITH_OPTIONALS ]] || return 1')
            self.add_options(options_with_optional_arg)

    def _get_all_option_strings(self, option):
        opts = []
        opts.extend(self.abbreviations.get_many_abbreviations(option.get_long_option_strings()))
        opts.extend(self.abbreviations.get_many_abbreviations(option.get_old_option_strings()))
        opts.extend(option.get_short_option_strings())
        return opts

    def add_options(self, options):
        options_with_when = []
        options_wout_when = []
        options_group_by_complete = OrderedDict()

        for option in options:
            if option.when:
                options_with_when.append(option)
            else:
                options_wout_when.append(option)

        for option in options_wout_when:
            complete = self.complete(option, False)
            if complete not in options_group_by_complete:
                options_group_by_complete[complete] = []
            options_group_by_complete[complete].append(option)

        if options_group_by_complete:
            r = 'case "$opt" in\n'
            for complete, options in options_group_by_complete.items():
                opts = []
                for option in options:
                    opts.extend(self._get_all_option_strings(option))

                r += '  %s)\n' % '|'.join(opts)
                if complete:
                    r += '%s\n' % utils.indent(complete, 4)
                r += '    return 0;;\n'
            r += 'esac'
            self.code.append(r)

        for option in options_with_when:
            opts = self._get_all_option_strings(option)
            completion_code = self.complete(option, False)

            cond = bash_when.generate_when_conditions(
                self.generator.commandline,
                self.generator.variable_manager,
                option.when)

            r  = 'case "$opt" in %s)\n' % '|'.join(opts)
            r += '  if %s; then\n' % cond
            if completion_code:
                r += '%s\n' % utils.indent(completion_code, 4)
            r += '    return 0\n'
            r += '  fi;;\n'
            r += 'esac'
            self.code.append(r)

    def get(self):
        if self.code:
            r  = '%s() {\n' % self.name
            r += '  local opt="$1" cur="$2" mode="$3"\n\n'
            r += '%s\n\n' % utils.indent('\n\n'.join(self.code), 2)
            r += '  return 1\n'
            r += '}'
            return r
        else:
            return None

def generate_option_completion(self):
    r = ''
    options = self.commandline.get_options(only_with_arguments=True)

    if self.commandline.abbreviate_options:
        # If we inherit options from parent commands, add those
        # to the abbreviation generator
        abbreviations = get_OptionAbbreviationGenerator(
            self.commandline.get_options(
                with_parent_options=self.commandline.inherit_options))
    else:
        abbreviations = utils.DummyAbbreviationGenerator()

    complete_option = MasterCompletionFunction(
        '__complete_option', options, abbreviations, self._complete_option, self)
    code = complete_option.get()

    if code:
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
      (LR        , '\n    __complete_option "$prev" "$cur" WITHOUT_OPTIONALS && return 0'),
      (G0        , ';;\n'),
      (G0        , '  -*)'),
      (OR        , '\n    __complete_option "$prev" "$cur" WITHOUT_OPTIONALS && return 0'),
      (SR        , '\n    case "$prev" in -%s[%s])' % (short_no_args_pattern, short_required_args)),
      (SR        , '\n      __complete_option "-${prev: -1}" "$cur" WITHOUT_OPTIONALS && return 0'),
      (SR        , '\n    esac'),
      (G0        , ';;\n'),
      (G0        , 'esac\n'),
      (G0        , '\n'),

      (G1        , 'case "$cur" in\n'),
      (G1        , '  --*=*)'),
      (LR|LO     , '\n    __complete_option "${cur%%=*}" "${cur#*=}" WITH_OPTIONALS && return 0'),
      (G1        , ';;\n'),
      (G1        , '  -*=*)'),
      (OR|OO     , '\n    __complete_option "${cur%%=*}" "${cur#*=}" WITH_OPTIONALS && return 0'),
      (G1        , ';;\n'),
      (G1        , '  --*);;\n'),
      (G1        , '  -*)'),
      (G2 and OLD, '\n    if ! __is_oldstyle_option "$cur"; then'),
      (G2        , '\n      local i'),
      (G2        , '\n      for ((i=2; i <= ${#cur}; ++i)); do'),
      (G2        , '\n        local pre="${cur:0:$i}" value="${cur:$i}"'),
      (SR|SO     , '\n        __complete_option "-${pre: -1}" "$value" WITH_OPTIONALS && {'),
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
