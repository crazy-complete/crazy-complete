'''This module contains code for validating the `complete` attribute'''

from .errors import CrazyError

def get_required_arg(args, name):
    try:
        return args.pop(0)
    except IndexError:
        raise CrazyError(f'Missing argument: {name}')

def get_optional_arg(args, default=None):
    try:
        return args.pop(0)
    except IndexError:
        return default

def require_no_more(args):
    if args:
        raise CrazyError(f'Too many arguments: {args}')

class CompletionValidator:
    @staticmethod
    def validate_complete(complete):
        if complete:
            complete = list(complete)
            command  = complete.pop(0)

            if not isinstance(command, str):
                raise CrazyError(f"Command is not a string: {command}")

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
                    '|'.join(option.option_strings),
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
        choices = get_required_arg(args, 'values')
        require_no_more(args)

        if hasattr(choices, 'items'):
            new_choices = {}
            for item, desc in choices.items():
                if not isinstance(item, (str, int, float)):
                    raise CrazyError(f'Item not a string/int/float: {item}')

                if not isinstance(desc, (str, int, float)):
                    raise CrazyError(f'Description not a string/int/float: {desc}')

                new_choices[str(item)] = str(desc)

            return (new_choices,)

        if isinstance(choices, (list, tuple)):
            new_choices = []
            for item in choices:
                if not isinstance(item, (str, int, float)):
                    raise CrazyError(f'Item not a string/int/float: {item}')

                new_choices.append(item)
            return (new_choices,)

        raise CrazyError('values: Not a list or dictionary')

    @staticmethod
    def command(args):
        require_no_more(args)
        return ()

    @staticmethod
    def directory(args):
        opts = get_optional_arg(args, {})
        require_no_more(args)

        directory = None
        for key, value in opts.items():
            if key == 'directory':
                if not isinstance(value, str):
                    raise CrazyError(f"directory: Not a string: {value}")

                directory = value
            else:
                raise CrazyError(f'Unknown option: {key}')

        return ({'directory': directory},)

    @staticmethod
    def file(args):
        opts = get_optional_arg(args, {})
        require_no_more(args)

        directory = None
        for key, value in opts.items():
            if key == 'directory':
                if not isinstance(value, str):
                    raise CrazyError(f"directory: Not a string: {value}")

                directory = value
            else:
                raise CrazyError(f'Unknown option: {key}')

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
        require_no_more(args)
        return ()

    @staticmethod
    def environment(args):
        require_no_more(args)
        return ()

    @staticmethod
    def exec(args):
        cmd = get_required_arg(args, 'command')
        require_no_more(args)

        if not isinstance(cmd, str):
            raise CrazyError(f"Command is not a string: {cmd}")

        return (cmd,)

    @staticmethod
    def value_list(args):
        opts = get_required_arg(args, 'options')
        require_no_more(args)

        values = None
        separator = ','

        for key, value in opts.items():
            if key == 'values':
                values = value
            elif key == 'separator':
                separator = value
            else:
                raise CrazyError(f'Unknown option: {key}')

        if values is None:
            raise CrazyError(f'Missing `values` option: {opts}')

        if not isinstance(values, (list, tuple)) and not hasattr(values, 'items'):
            raise CrazyError(f'values: not a list|dictionary: {values}')

        if len(values) == 0:
            raise CrazyError(f'values: cannot be empty')

        if hasattr(values, 'items'):
            for item, desc in values.items():
                if not isinstance(item, str):
                    raise CrazyError(f'values: Not a string: {item}')

                if not isinstance(desc, str):
                    raise CrazyError(f'values: Not a string: {desc}')
        else:
            for index, value in enumerate(values):
                if not isinstance(value, str):
                    raise CrazyError(f'values[{index}]: Not a string: {value}')

        if not isinstance(separator, str):
            raise CrazyError(f'separator: Not a string: {separator}')

        if len(separator) != 1:
            raise CrazyError(f'Invalid length for separator: {separator}')

        return ({'values': values, 'separator': separator},)
