'''
Code for generating a bash auto completion file
'''

from collections import OrderedDict

from . import generation_notice
from . import modeline
from . import shell
from . import utils
from . import when
from . import helpers
from . import bash_helpers
from . import bash_complete
from . import bash_parser
from .bash_utils import *

class VariableUsageTracer:
    def __init__(self):
        self.have = []
        self.values = []

    def make_have_variable(self, option):
        if option not in self.have:
            self.have.append(option)
        return make_option_variable_name(option, prefix='HAVE_')

    def make_value_variable(self, option):
        if option not in self.values:
            self.values.append(option)
        return make_option_variable_name(option, prefix='VALUE_')

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
            if option.takes_args == '?':
                options_with_optional_arg.append(option)
            elif option.takes_args:
                options_with_required_arg.append(option)

        self.add_options(options_with_required_arg)
        if options_with_optional_arg:
            self.code.append('[[ "$mode" == WITH_OPTIONALS ]] || return 1')
            self.code.append('')
            self.add_options(options_with_optional_arg)

    def add_options(self, options):
        for option in options:
            opts = []
            opts.extend(self.abbreviations.get_many_abbreviations(option.get_long_option_strings()))
            opts.extend(self.abbreviations.get_many_abbreviations(option.get_old_option_strings()))
            opts.extend(option.get_short_option_strings())

            completion_code = self.complete(option, False)

            r  = 'case "$opt" in %s)\n' % '|'.join(opts)
            # TODO: add when
            if completion_code:
                r += '%s\n' % utils.indent(completion_code, 2)
            r += '  return 0;;\n'
            r += 'esac\n'
            self.code.append(r)

    def get(self):
        if self.code:
            r  = '%s() {\n' % self.name
            r += '  local opt="$1" cur="$2" mode="$3"\n\n'
            r += '%s\n' % utils.indent('\n'.join(self.code), 2)
            r += '  return 1\n'
            r += '}'
            return r
        else:
            return None

class BashCompletionGenerator:
    def __init__(self, ctxt, commandline):
        self.commandline = commandline
        self.ctxt        = ctxt
        self.options     = commandline.get_options()
        self.positionals = commandline.get_positionals()
        self.subcommands = commandline.get_subcommands_option()
        self.completer   = bash_complete.BashCompleter()
        self.captured_variables = VariableUsageTracer()
        self._complete_commandline()

    def _complete_action(self, action, append=True):
        context = self.ctxt.getOptionGenerationContext(self.commandline, action)
        return self.completer.complete(context, *action.complete).get_code(append)

    def _generate_commandline_parsing(self):
        options = self.commandline.get_options(with_parent_options=True)

        local_have_vars = ['%s=0' % make_option_variable_name(o, 'HAVE_') for o in options]
        local_value_vars = [make_option_variable_name(o, 'VALUE_') for o in options]

        r = 'local END_OF_OPTIONS POSITIONALS POSITIONAL_NUM\n'

        if local_have_vars:
            r += 'local %s\n' % ' '.join(local_have_vars)

        if local_value_vars:
            r += 'local %s\n' % ' '.join(local_value_vars)

        r +=  '\n%s' % self.ctxt.helpers.use_function('parse_commandline')
        return r

    def _find_options(self, option_strings):
        result = []

        for option_string in option_strings:
            found = False
            for option in self.options:
                if option_string in option.option_strings:
                    if option not in result:
                        result.append(option)
                    found = True
                    break
            if not found:
                raise Exception('Option %r not found' % option_string)

        return result

    def _generate_when_conditions(self, when_):
        parsed = when.parse_when(when_)

        if isinstance(parsed, when.OptionIs):
            conditions = []

            for o in self._find_options(parsed.options):
                have_option = '(( %s ))' % self.captured_variables.make_have_variable(o)
                value_equals = []
                for value in parsed.values:
                    value_equals.append('[[ "$%s" == %s ]]' % (
                        self.captured_variables.make_value_variable(o),
                        shell.escape(value)
                    ))

                if len(value_equals) == 1:
                    cond = '{ %s && %s; }' % (have_option, value_equals[0])
                else:
                    cond = '{ %s && { %s; } }' % (have_option, ' || '.join(value_equals))

                conditions.append(cond)

            if len(conditions) == 1:
                return conditions[0]
            else:
                return '{ %s; }' % ' || '.join(conditions)

        elif isinstance(parsed, when.HasOption):
            conditions = []

            for o in self._find_options(parsed.options):
                cond = '(( %s ))' % self.captured_variables.make_have_variable(o)
                conditions.append(cond)

            if len(conditions) == 1:
                return conditions[0]
            else:
                return '{ %s; }' % ' || '.join(conditions)
        else:
            raise Exception('invalid instance of `parse`')

    def _generate_option_strings_completion(self):
        r  = 'if (( ! END_OF_OPTIONS )) && [[ "$cur" = -* ]]; then\n'
        r += '  local -a opts=()\n'
        for option in self.options:
            option_guard = []

            if not option.multiple_option:
                option_guard += ["! %s" % self.captured_variables.make_have_variable(option)]

            for exclusive_option in option.get_conflicting_options():
                option_guard += ["! %s" % self.captured_variables.make_have_variable(exclusive_option)]

            if option_guard:
                option_guard = '(( %s )) && ' % ' && '.join(option_guard)
            else:
                option_guard = ''

            when_guard = ''
            if option.when is not None:
                when_guard = self._generate_when_conditions(option.when)
                when_guard = '%s && ' % when_guard

            r += '  %s%sopts+=(%s)\n' % (option_guard, when_guard, ' '.join(shell.escape(o) for o in option.option_strings))
        r += '  %s -a -- "$cur" "${opts[@]}"\n' % self.ctxt.helpers.use_function('compgen_w_replacement')
        r += '  return 1\n'
        r += 'fi'
        return r

    def _generate_option_completion(self):
        r = ''
        options = self.commandline.get_options(only_with_arguments=True)

        if self.commandline.abbreviate_options:
            # TODO: describe why we use with_parent_options=True here
            # TODO: with_parent_options only if inherit_options is true
            abbreviations = get_OptionAbbreviationGenerator(
                self.commandline.get_options(with_parent_options=True))
        else:
            abbreviations = utils.DummyAbbreviationGenerator()

        complete_option = MasterCompletionFunction('__complete_option', options, abbreviations, self._complete_action, self)
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
                if option.takes_args is True:
                    LR = True
                elif option.takes_args == '?':
                    LO = True

            if option.get_old_option_strings():
                if option.takes_args is True:
                    OR = True
                elif option.takes_args == '?':
                    OO = True

            if option.get_short_option_strings():
                if option.takes_args is True:
                    SR = True
                elif option.takes_args == '?':
                    SO = True

        G0 = LR or OR or SR
        G1 = LR or LO or OR or OO or SR or SO
        G2 = SR or SO

        prefix_compreply_func = ''
        if G2:
            prefix_compreply_func = self.ctxt.helpers.use_function('prefix_compreply')

        is_oldstyle_option = None
        if G2:
            all_options = utils.flatten(abbreviations.get_many_abbreviations(
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
            if option.takes_args is True:
                short_required_args += ''.join(o.lstrip('-') for o in option.get_short_option_strings())
            elif option.takes_args is False:
                short_no_args += ''.join(o.lstrip('-') for o in option.get_short_option_strings())

        code = [
          # CONDITION, TEXT
          (G0        , 'case "$prev" in\n'),
          (G0        , '  --*)'),
          (LR        , '\n    __complete_option "$prev" "$cur" WITHOUT_OPTIONALS && return 0'),
          (G0        , ';;\n'),
          (G0        , '  -*)'),
          (OR        , '\n    __complete_option "$prev" "$cur" WITHOUT_OPTIONALS && return 0'),
          (SR        , '\n    case "$prev" in -*([%s])[%s])' % (short_no_args, short_required_args)),
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

    def _generate_positionals_completion(self):
        def make_block(code):
            if code:
                return '{\n%s\n  return 0;\n}' % utils.indent(code, 2)
            else:
                return '{\n  return 0;\n}'

        r = ''
        for positional in self.positionals:
            operator = '-eq'
            if positional.repeatable:
                operator = '-ge'
            r += 'test "$POSITIONAL_NUM" %s %d && ' % (operator, positional.get_positional_num())
            if positional.when:
                r += '%s && ' % self._generate_when_conditions(positional.when)
            r += '%s\n\n' % make_block(self._complete_action(positional, False))

        if self.subcommands:
            cmds = self.subcommands.get_choices().keys()
            complete = self.completer.choices(self.ctxt, cmds).get_code()
            r += 'test "$POSITIONAL_NUM" -eq %d && ' % self.subcommands.get_positional_num()
            r += '%s\n\n' % make_block(complete)
        return r.strip()

    def _generate_subcommand_call(self):
        # This code is used to call subcommand functions

        r  = 'if (( %i < POSITIONAL_NUM )); then\n' % (self.subcommands.get_positional_num() - 1)
        r += '  case "${POSITIONALS[%i]}" in\n' % (self.subcommands.get_positional_num() - 1)
        for subcommand in self.subcommands.subcommands:
            cmds = utils.get_all_command_variations(subcommand)
            pattern = '|'.join(shell.escape(s) for s in cmds)
            if self.commandline.inherit_options:
                r += '    %s) %s && return 0;;\n' % (pattern, shell.make_completion_funcname(subcommand))
            else:
                r += '    %s) %s && return 0 || return 1;;\n' % (pattern, shell.make_completion_funcname(subcommand))
        r += '  esac\n'
        r += 'fi'
        return r

    def _complete_commandline(self):
        # The completion function returns 0 (success) if there was a completion match.
        # This return code is used for dealing with subcommands.

        if not utils.is_worth_a_function(self.commandline):
            r  = '%s() {\n' % shell.make_completion_funcname(self.commandline)
            r += '  return 0\n'
            r += '}'
            self.result = r
            return

        code = OrderedDict()

        if self.commandline.parent is None:
            # The root parser makes those variables local and sets up the completion.
            r  = 'local cur prev words cword split\n'
            r += '_init_completion -n = || return'
            code['init_completion'] = r

            c = bash_parser.generate(self.commandline)
            func = helpers.ShellFunction('parse_commandline', c)
            self.ctxt.helpers.add_function(func)

        # Here we want to parse commandline options. We set this to None because
        # we have to delay this call for collecting info.
        code['command_line_parsing'] = None

        if self.subcommands:
            code['subcommand_call'] = self._generate_subcommand_call()

        if len(self.options):
            # This code is used to complete arguments of options
            code['option_completion'] = self._generate_option_completion()

            # This code is used to complete option strings (--foo, ...)
            code['option_strings_completion'] = self._generate_option_strings_completion()

        if len(self.positionals) or self.subcommands:
            # This code is used to complete positionals
            code['positional_completion'] = self._generate_positionals_completion()

        # This sets up END_OF_OPTIONS, POSITIONALS, POSITIONAL_NUM and the HAVE_* variables.
        code['command_line_parsing'] = self._generate_commandline_parsing()

        r  = '%s() {\n' % shell.make_completion_funcname(self.commandline)
        r += '%s\n\n'   % utils.indent('\n\n'.join(c for c in code.values() if c), 2)
        r += '  return 1\n'
        r += '}'

        self.result = r

def generate_completion(commandline, program_name=None, config=None):
    result = shell.CompletionGenerator(
        BashCompletionGenerator,
        bash_helpers.BashHelpers,
        commandline,
        program_name,
        config)

    commandline = result.result[0].commandline

    output = []
    output += [generation_notice.GENERATION_NOTICE]
    output += result.include_files_content
    output += result.ctxt.helpers.get_used_functions_code()
    output += [r.result for r in result.result]
    output += ['complete -F %s %s' % (shell.make_completion_funcname(commandline), commandline.prog)]
    if config.vim_modeline:
        output += [modeline.get_vim_modeline('sh')]

    return '\n\n'.join(output)
