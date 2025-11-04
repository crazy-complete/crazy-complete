'''Module for positionals completion in Bash.'''

from . import algo
from . import bash_when
from .str_utils import indent


def _make_block(code):
    if not code:
        return '{\n  return 0;\n}'

    return '{\n%s\n  return 0;\n}' % indent(code, 2)


def _is_not_command_arg(positional):
    return (
        not positional.complete or
        positional.complete[0] != 'command_arg'
    )


def _generate_subcommand_positional(generator):
    cmds = generator.subcommands.get_choices().keys()
    complete = generator.completer.choices(generator.ctxt, [], cmds).get_code()
    return '(( ${#POSITIONALS[@]} == %d )) && %s' % (
        generator.subcommands.get_positional_num(),
        _make_block(complete))


def _get_positional_condition(positional):
    op = '=='
    if positional.repeatable:
        op = '>='
    return '${#POSITIONALS[@]} %s %s' % (op, positional.get_positional_num())


def _generate_positionals_with_when(generator):
    code = []

    positionals = filter(_is_not_command_arg, generator.positionals)

    for positional in positionals:
        condition = _get_positional_condition(positional)
        r = '(( %s )) && ' % condition
        if positional.when:
            r += '%s && ' % bash_when.generate_when_conditions(
                generator.commandline,
                generator.variable_manager,
                positional.when)
        r += '%s' % _make_block(generator._complete_option(positional))

        code.append(r)

    return '\n\n'.join(code)


def _generate_positionals_without_when(generator):
    code = []

    positionals = filter(_is_not_command_arg, generator.positionals)

    grouped_by_complete = algo.group_by(
        positionals, generator._complete_option)

    for complete, positionals in grouped_by_complete.items():
        conditions = [_get_positional_condition(p) for p in positionals]
        r = '(( %s )) && ' % ' || '.join(conditions)
        r += '%s' % _make_block(complete)
        code.append(r)

    return '\n\n'.join(code)


def generate(generator):
    '''Generate code for completing positionals.'''

    code = []

    has_when = any(p.when for p in generator.positionals)

    if has_when:
        code += [_generate_positionals_with_when(generator)]
    else:
        code += [_generate_positionals_without_when(generator)]

    if generator.subcommands:
        code += [_generate_subcommand_positional(generator)]

    return '\n\n'.join(c for c in code if c)
