def get_required_arg(l, name):
    try:
        return l.pop(0)
    except:
        raise Exception(f'Missing argument: {name}')

def get_optional_arg(l, default=None):
    try:
        return l.pop(0)
    except:
        return default

def require_no_more(l):
    if l:
        raise Exception('Too many arguments')

class CompletionValidator:
    @staticmethod
    def validate_complete(complete):
        if complete:
            complete = list(complete)
            command  = complete.pop(0)

            if not hasattr(CompletionValidator, command):
                raise Exception(f"Unknown completion command: {command}")

            getattr(CompletionValidator, command)(complete)

    @staticmethod
    def validate_commandline(cmdline):
        for option in cmdline.get_options():
            try:
                CompletionValidator.validate_complete(option.complete)
            except Exception as e:
                raise Exception("%s: %s: %s" % (
                    cmdline.prog,
                    ' '.join(option.option_strings),
                    e))

        for positional in cmdline.get_positionals():
            try:
                CompletionValidator.validate_complete(positional.complete)
            except Exception as e:
                raise Exception("%s: %d (%s): %s" % (
                    cmdline.prog,
                    positional.number,
                    positional.metavar,
                    e))

    @staticmethod
    def validate_commandlines(cmdline):
        cmdline.visit_commandlines(lambda o: CompletionValidator.validate_commandline(o))

    @staticmethod
    def none(args):
        return args

    @staticmethod
    def choices(args):
        choices = get_required_arg(args, 'VALUES')
        require_no_more(args)

        if hasattr(choices, 'items'):
            new_choices = {}
            for item, desc in choices.items():
                if not isinstance(item, (str, int, float)):
                    raise Exception(f'Item not a str/int/float: {item}')

                if not isinstance(desc, (str, int, float)):
                    raise Exception(f'Description not a str/int/float: {desc}')

                new_choices[str(item)] = str(desc)

            return (new_choices,)

        if isinstance(choices, (list, tuple)):
            new_choices = []
            for item in choices:
                if not isinstance(item, (str, int, float)):
                    raise Exception(f'Item not a str/int/float: {item}')

                new_choices.append(item)
            return (new_choices,)

        raise Exception('VALUES: Not a list, tuple or dictionary')

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
                    raise Exception(f"directory: Not a str: {value}")

                directory = value
            else:
                raise Exception(f'Unknown option: {name}')

        return ({'directory': directory},)

    @staticmethod
    def file(args):
        opts = get_optional_arg(args, {})
        require_no_more(args)

        directory = None
        for name, value in opts.items():
            if name == 'directory':
                if not isinstance(value, str):
                    raise Exception(f"directory: Not a str: {value}")

                directory = value
            else:
                raise Exception(f'Unknown option: {name}')

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
        for arg in args:
            if not isinstance(arg, int):
                raise Exception(f"Not an int: {arg}")

        if len(args) == 2:
            start, stop = args
            if start > stop:
                raise Exception(f"start > stop: {start} > {stop}")

            return (start, stop, 1)

        if len(args) == 3:
            # TODO: check
            return args

        raise Exception('Invalid number of arguments')

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
        try:    option = args.pop(0)
        except: option = None
        require_no_more(args)
        if option not in (None, '-x'):
            raise Exception(f'Invalid option: {option}')
        return ()

    @staticmethod
    def exec(args):
        cmd = get_required_arg(args, 'COMMAND')
        require_no_more(args)

        if not isinstance(cmd, str):
            raise Exception(f"Command is not a str: {cmd}")

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
                raise Exception(f'Invalid key: {key}')

        if values is None:
            raise Exception(f'Missing `values` key: {opts}')

        if not isinstance(values, (list, tuple)):
            raise Exception(f'Values: not a list: {values}')

        for value in values:
            if not isinstance(value, (str, int, float)):
                raise Exception(f'Invalid value: {value}')

        if len(separator) != 1:
            raise Exception(f'Invalid length for separator: {separator}')

        return ({'values': values, 'separator': separator},)
