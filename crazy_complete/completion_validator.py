''' This module contains code for validating the `complete` attribute '''

from .errors import CrazyError

def get_required_arg(l, name):
    try:
        return l.pop(0)
    except IndexError:
        raise CrazyError(f'Missing argument: {name}')

def get_optional_arg(l, default=None):
    try:
        return l.pop(0)
    except IndexError:
        return default

def require_no_more(l):
    if l:
        raise CrazyError('Too many arguments')

class CompletionValidator:
    @staticmethod
    def validate_complete(complete):
        if complete:
            complete = list(complete)
            command  = complete.pop(0)

            if not hasattr(CompletionValidator, command):
                raise CrazyError(f"Unknown command for `complete`: {command}")

            getattr(CompletionValidator, command)(complete)

    @staticmethod
    def validate_commandline(cmdline):
        for option in cmdline.get_options():
            try:
                CompletionValidator.validate_complete(option.complete)
            except CrazyError as e:
                raise CrazyError("%s: %s: %s" % (
                    cmdline.get_command_path(),
                    ' '.join(option.option_strings),
                    e))

        for positional in cmdline.get_positionals():
            try:
                CompletionValidator.validate_complete(positional.complete)
            except CrazyError as e:
                raise CrazyError("%s: %d (%s): %s" % (
                    cmdline.get_command_path(),
                    positional.number,
                    positional.metavar,
                    e))

    @staticmethod
    def validate_commandlines(cmdline):
        cmdline.visit_commandlines(lambda o: CompletionValidator.validate_commandline(o))

    @staticmethod
    def none(args):
        return ()

    @staticmethod
    def choices(args):
        choices = get_required_arg(args, 'VALUES')
        require_no_more(args)

        if hasattr(choices, 'items'):
            new_choices = {}
            for item, desc in choices.items():
                if not isinstance(item, (str, int, float)):
                    raise CrazyError(f'Item not a str/int/float: {item}')

                if not isinstance(desc, (str, int, float)):
                    raise CrazyError(f'Description not a str/int/float: {desc}')

                new_choices[str(item)] = str(desc)

            return (new_choices,)

        if isinstance(choices, (list, tuple)):
            new_choices = []
            for item in choices:
                if not isinstance(item, (str, int, float)):
                    raise CrazyError(f'Item not a str/int/float: {item}')

                new_choices.append(item)
            return (new_choices,)

        raise CrazyError('VALUES: Not a list, tuple or dictionary')

    @staticmethod
    def command(args):
        require_no_more(args)
        return ()

    @staticmethod
    def directory(args):
        opts = get_optional_arg(args, {})
        require_no_more(args)

        directory = None
        for name, value in opts.items():
            if name == 'directory':
                if not isinstance(value, str):
                    raise CrazyError(f"directory: Not a str: {value}")

                directory = value
            else:
                raise CrazyError(f'Unknown option: {name}')

        return ({'directory': directory},)

    @staticmethod
    def file(args):
        opts = get_optional_arg(args, {})
        require_no_more(args)

        directory = None
        for name, value in opts.items():
            if name == 'directory':
                if not isinstance(value, str):
                    raise CrazyError(f"directory: Not a str: {value}")

                directory = value
            else:
                raise CrazyError(f'Unknown option: {name}')

        return ({'directory': directory},)

    @staticmethod
    def group(args):
        require_no_more(args)
        return ()

    @staticmethod
    def hostname(args):
        require_no_more(args)
        return ()

    @staticmethod
    def pid(args):
        require_no_more(args)
        return ()

    @staticmethod
    def process(args):
        require_no_more(args)
        return ()

    @staticmethod
    def range(args):
        start = get_required_arg(args, "start")
        stop  = get_required_arg(args, "stop")
        step  = get_optional_arg(args, 1)
        require_no_more(args)

        if not isinstance(start, int):
            raise CrazyError(f"start: not an int: {start}")

        if not isinstance(stop, int):
            raise CrazyError(f"stop: not an int: {stop}")

        if not isinstance(step, int):
            raise CrazyError(f"step: not an int: {step}")

        if step > 0:
            if start > stop:
                raise CrazyError(f"start > stop: {start} > {stop} (step={step})")
        elif step < 0:
            if stop > start:
                raise CrazyError(f"stop > start: {stop} > {start} (step={step})")
        else:
            raise CrazyError(f"step: cannot be 0")

        return args

    @staticmethod
    def user(args):
        require_no_more(args)
        return ()

    @staticmethod
    def signal(args):
        require_no_more(args)
        return ()

    @staticmethod
    def service(args):
        require_no_more(args)
        return ()

    @staticmethod
    def variable(args):
        option = get_optional_arg(args, None)
        require_no_more(args)
        if option not in (None, '-x'):
            raise CrazyError(f'Invalid option: {option}')
        return ()

    @staticmethod
    def exec(args):
        cmd = get_required_arg(args, 'COMMAND')
        require_no_more(args)

        if not isinstance(cmd, str):
            raise CrazyError(f"Command is not a str: {cmd}")

        return (cmd,)

    @staticmethod
    def value_list(args):
        opts = get_required_arg(args, 'OPTIONS')
        require_no_more(args)

        values    = None
        separator = ','

        for key, value in opts.items():
            if key == 'values':
                values = value
            elif key == 'separator':
                separator = value
            else:
                raise CrazyError(f'Invalid key: {key}')

        if values is None:
            raise CrazyError(f'Missing `values` key: {opts}')

        if not isinstance(values, (list, tuple)):
            raise CrazyError(f'Values: not a list: {values}')

        for value in values:
            if not isinstance(value, (str, int, float)):
                raise CrazyError(f'Invalid value: {value}')

        if len(separator) != 1:
            raise CrazyError(f'Invalid length for separator: {separator}')

        return ({'values': values, 'separator': separator},)
