'''Module for option completion in Bash.'''

from . import algo
from . import utils
from . import bash_when
from . import bash_utils
from . import bash_patterns
from .str_utils import indent


class MasterCompletionFunction:
    '''Class for generating a master completion function.'''

    def __init__(self, options, abbreviations, generator):
        self.abbreviations = abbreviations
        self.complete = generator._complete_option
        self.generator = generator
        self.optionals = False
        self.code = []

        optional_arg = list(filter(lambda o: o.complete and o.optional_arg is True, options))
        required_arg = list(filter(lambda o: o.complete and o.optional_arg is False, options))

        self._add_options(required_arg)

        if optional_arg:
            self.optionals = True
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
                r += '  %s)\n' % bash_patterns.make_pattern(opts)
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

            r  = 'case "$opt" in %s)\n' % bash_patterns.make_pattern(opts)
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
            if self.optionals:
                r += '  local opt="$1" cur="$2" mode="$3"\n\n'
            else:
                r += '  local opt="$1" cur="$2"\n\n'
            r += '%s\n\n' % indent('\n\n'.join(self.code), 2)
            r += '  return 1\n'
            r += '}'
            return r

        return None


class MasterCompletionFunctionNoWhen:
    '''Class for generating a master completion function.'''

    def __init__(self, options, abbreviations, generator):
        self.abbreviations = abbreviations
        self.complete = generator._complete_option
        self.generator = generator
        self.optionals = False
        self.code = []

        optional_arg = list(filter(lambda o: o.complete and o.optional_arg is True, options))
        required_arg = list(filter(lambda o: o.complete and o.optional_arg is False, options))

        self._add_options(required_arg)

        if optional_arg:
            self.optionals = True
            r =  '(( ! ret )) && return 0\n'
            r += '[[ "$mode" == WITH_OPTIONAL ]] || return 1\n'
            r += 'ret=0'
            self.code.append(r)
            self._add_options(optional_arg)

    @staticmethod
    def accept(options):
        return not any(option.when for option in options)

    def _get_all_option_strings(self, option):
        opts = []
        opts.extend(self.abbreviations.get_many_abbreviations(option.get_long_option_strings()))
        opts.extend(self.abbreviations.get_many_abbreviations(option.get_old_option_strings()))
        opts.extend(option.get_short_option_strings())
        return opts

    def _add_options(self, options):
        options_group_by_complete = algo.group_by(options, lambda o: self.complete(o, False))

        if options_group_by_complete:
            r = 'case "$opt" in\n'
            for complete, options in options_group_by_complete.items():
                opts = algo.flatten([self._get_all_option_strings(o) for o in options])
                if complete:
                    r += '  %s)\n' % bash_patterns.make_pattern(opts)
                    r += '%s;;\n' % indent(complete, 4)
                else:
                    r += '  %s);;\n' % bash_patterns.make_pattern(opts)
            r += '  *) ret=1;;\n'
            r += 'esac'
            self.code.append(r)

    def get(self, funcname):
        '''Get the function code.'''

        if self.code:
            r  = '%s() {\n' % funcname
            if self.optionals:
                r += '  local opt="$1" cur="$2" mode="$3" ret=0\n\n'
            else:
                r += '  local opt="$1" cur="$2" ret=0\n\n'
            r += '%s\n\n' % indent('\n\n'.join(self.code), 2)
            r += '  return $ret\n'
            r += '}'
            return r

        return None


def _get_master_completion_obj(options, abbreviations, generator):
    if MasterCompletionFunctionNoWhen.accept(options):
        klass = MasterCompletionFunctionNoWhen
    else:
        klass = MasterCompletionFunction

    return klass(options, abbreviations, generator)


class _Info:
    def __init__(self, options, abbreviations, commandline, ctxt):
        self.commandline    = commandline
        self.ctxt           = ctxt
        self.short_required = False # Short with required argument
        self.short_optional = False # Short with optional argument
        self.long_required  = False # Long with required argument
        self.long_optional  = False # Long with optional argument
        self.old_required   = False # Old-Style with required argument
        self.old_optional   = False # Old-Style with optional argument

        self._collect_options_info(options)

        all_options = self.commandline.get_options(
            with_parent_options=self.commandline.inherit_options)

        old_option_strings = algo.flatten([o.get_old_option_strings() for o in all_options])
        old_option_strings = abbreviations.get_many_abbreviations(old_option_strings)
        self.old_option_strings = bash_utils.CasePatterns.for_old_without_arg(old_option_strings)

        self.short_no_args = ''
        self.short_required_args = ''
        self.short_optional_args = ''

        for option in all_options:
            short_opts = ''.join(o.lstrip('-') for o in option.get_short_option_strings())

            if option.complete and option.optional_arg is False:
                self.short_required_args += short_opts
            elif option.complete and option.optional_arg is True:
                self.short_optional_args += short_opts
            elif option.complete is None:
                self.short_no_args += short_opts

        if self.short_no_args:
            self.short_no_args_pattern = '*([%s])' % self.short_no_args
        else:
            self.short_no_args_pattern = ''

    def _collect_options_info(self, options):
        for option in options:
            if option.get_long_option_strings():
                if option.complete and option.optional_arg is True:
                    self.long_optional = True
                elif option.complete:
                    self.long_required = True

            if option.get_old_option_strings():
                if option.complete and option.optional_arg is True:
                    self.old_optional = True
                elif option.complete:
                    self.old_required = True

            if option.get_short_option_strings():
                if option.complete and option.optional_arg is True:
                    self.short_optional = True
                elif option.complete:
                    self.short_required = True


def _get_prev_completion(info):
    r =  'case "$prev" in\n'

    if info.long_required:
        r += '  --*) __complete_option "$prev" "$cur" WITHOUT_OPTIONAL && return 0;;\n'
    else:
        r += '  --*);;\n'

    if info.old_required and info.short_required:
        r += '  -*)  __complete_option "$prev" "$cur" WITHOUT_OPTIONAL && return 0;&\n'
        r += '  -%s[%s])\n' % (info.short_no_args_pattern, info.short_required_args)
        r += '       __complete_option "-${prev: -1}" "$cur" WITHOUT_OPTIONAL && return 0;;\n'
    elif info.old_required:
        r += '  -*)  __complete_option "$prev" "$cur" WITHOUT_OPTIONAL && return 0;;\n'
    elif info.short_required:
        r += '  -%s[%s])\n' % (info.short_no_args_pattern, info.short_required_args)
        r += '       __complete_option "-${prev: -1}" "$cur" WITHOUT_OPTIONAL && return 0;;\n'

    r += 'esac'
    return r


def _get_cur_completion(info):
    r =  'case "$cur" in\n'

    if info.long_required or info.long_optional:
        r += '  --*=*)\n'
        r += '    __complete_option "${cur%%=*}" "${cur#*=}" WITH_OPTIONAL && return 0;;\n'
    else:
        r += '  --*=*);;\n'

    r += '  --*);;\n'

    if (info.short_required or info.short_optional) and info.old_option_strings:
        r += '  %s);;\n' % info.old_option_strings

    if info.old_required or info.old_optional:
        r += '  -*=*)\n'
        r += '    __complete_option "${cur%%=*}" "${cur#*=}" WITH_OPTIONAL && return 0;&\n'

    if info.short_required or info.short_optional:
        r += '  -%s[%s%s]*)\n' % (info.short_no_args_pattern, info.short_required_args, info.short_optional_args)
        r += '    local i\n'
        r += '    for ((i=2; i <= ${#cur}; ++i)); do\n'
        r += '      local pre="${cur:0:$i}" value="${cur:$i}"\n'
        r += '      __complete_option "-${pre: -1}" "$value" WITH_OPTIONAL && {\n'
        r += '        %s "$pre"\n' % info.ctxt.helpers.use_function('prefix_compreply')
        r += '        return 0\n'
        r += '      }\n'
        r += '    done;;\n'

    # Optimization: Strip unused case patterns at the end
    if r.endswith('  -*=*);;\n'):
        r = r.replace('  -*=*);;\n', '')

    if r.endswith('  --*);;\n'):
        r = r.replace('  --*);;\n', '')

    r += 'esac'
    return r


def _get_dispatcher(info):
    r = []

    if info.short_required or info.long_required or info.old_required:
        r += [_get_prev_completion(info)]

    if info.short_required or info.long_required or info.old_required or \
       info.short_optional or info.long_optional or info.old_optional:
        r += [_get_cur_completion(info)]

    return '\n\n'.join(r)


def generate_option_completion(self):
    options = self.commandline.get_options(only_with_arguments=True)
    abbreviations = utils.get_option_abbreviator(self.commandline)

    complete_function = _get_master_completion_obj(options, abbreviations, self)
    complete_function_code = complete_function.get('__complete_option')

    if not complete_function_code:
        return None

    info = _Info(options, abbreviations, self.commandline, self.ctxt)
    dispatcher_code = _get_dispatcher(info)

    if not complete_function.optionals:
        dispatcher_code = dispatcher_code.replace('WITH_OPTIONAL ', '')
        dispatcher_code = dispatcher_code.replace('WITHOUT_OPTIONAL ', '')

    return f'{complete_function_code}\n\n{dispatcher_code}'
