#!/usr/bin/python3

def get_required_arg(l, name):
    try:
        return l.pop(0)
    except:
        raise Exception('Missing argument: %s' % name)

def require_no_more(l):
    if len(l):
        raise Exception('Too many arguments')

class CompletionValidator:
    def _validate_commandline(self, cmdline):
        for option in cmdline.get_options():
            if option.complete:
                complete = list(option.complete)
                command  = complete.pop(0)

                try:
                    if not hasattr(self, command):
                        raise Exception("Unknown completion command: %r" % command)

                    getattr(self, command)(complete)
                except Exception as e:
                    raise Exception("%s: %s: %s" % (
                        cmdline.prog,
                        ' '.join(option.option_strings),
                        e))

        for positional in cmdline.get_positionals():
            if positional.complete:
                complete = list(positional.complete)
                command  = complete.pop(0)

                try:
                    if not hasattr(self, command):
                        raise Exception("Unknown completion command: %r" % command)

                    getattr(self, command)(complete)
                except Exception as e:
                    raise Exception("%s: %s: %s" % (cmdline.prog, positional.metavar, e))


    def validate_commandlines(self, cmdline):
        self._validate_commandline(cmdline)
        if cmdline.get_subcommands_option():
            for subcommand in cmdline.get_subcommands_option().subcommands:
                self.validate_commandlines(subcommand)

    def none(self, a):
        return a

    def choices(self, a):
        choices = get_required_arg(a, 'VALUES')
        require_no_more(a)

        if hasattr(choices, 'items'):
            new_choices = {}
            for item, descr in choices.items():
                if not isinstance(item, (str, int, float)):
                    raise Exception('Item not a str/int/float: %r' % item)

                if not isinstance(descr, (str, int, float)):
                    raise Exception('Description not a str/int/float: %r' % descr)

                new_choices[str(item)] = str(descr)

            return (new_choices,)
        elif isinstance(choices, (list, tuple)):
            new_choices = []
            for item in choices:
                if not isinstance(item, (str, int, float)):
                    raise Exception('Item not a str/int/float: %r' % item)

                new_choices.append(item)
            return (new_choices,)
        else:
            raise Exception('VALUES: Not a list')

    def command(self, a):
        require_no_more(a)
        return ()
            
    def directory(self, a):
        try:    opts = a.pop(0)
        except: opts = {}
        require_no_more(a)

        directory = None
        for name, value in opts.items():
            if name == 'directory':
                if not isinstance(value, str):
                    raise Exception("Not a str: %r" % value)

                directory = value
            else:
                raise Exception('Unknown option: %s' % name)

        return ({'directory': directory},)

    def file(self, a):
        try:    opts = a.pop(0)
        except: opts = {}
        require_no_more(a)

        directory = None
        for name, value in opts.items():
            if name == 'directory':
                if not isinstance(value, str):
                    raise Exception("Not a str: %r" % value)

                directory = value
            else:
                raise Exception('Unknown option: %s' % name)

        return ({'directory': directory},)

    def group(self, a):
        require_no_more(a)
        return ()

    def hostname(self, a):
        require_no_more(a)
        return ()

    def pid(self, a):
        require_no_more(a)
        return ()

    def process(self, a):
        require_no_more(a)
        return ()

    def range(self, a):
        for arg in a:
            if not isinstance(arg, int):
                raise Exception("Not an int: %r" % arg)

        if len(a) == 2:
            start, stop = a
            if start > stop:
                raise Exception("Start > stop: %r > %r" % (start, stop))

            return (start, stop, 1)
        elif len(a) == 3:
            # TODO: check
            return a

    def user(self, a):
        require_no_more(a)
        return ()

    def signal(self, a):
        require_no_more(a)
        return ()

    def service(self, a):
        require_no_more(a)
        return ()

    def variable(self, a):
        try:    option = a.pop(0)
        except: option = None
        require_no_more(a)
        if option not in (None, '-x'):
            raise Exception('Invalid option: %r' % option)
        return ()

    def exec(self, a):
        cmd = get_required_arg(a, 'COMMAND')
        require_no_more(a)

        if not isinstance(cmd, str):
            raise Exception("Cmd is not a str: %r" % cmd)

        return (cmd,)

    def value_list(self, a):
        opts = get_required_arg(a, 'OPTIONS')
        require_no_more(a)

        values = None
        separator = None

        for key, value in opts.items():
            if key == 'values':      values = value
            elif key == 'separator': separator = value
            else: raise Exception('Invalid key: %r' % key)

        if values is None:
            raise Exception('Missing `values` key: %r' % opts)

        if not isinstance(values, (list, tuple)):
            raise Exception('Values: not a list' % values)

        for value in values:
            if not isinstance(value, (str, int, float)):
                raise Exception('Invalid value: %r' % value)

        if separator is not None:
            if len(separator) != 1:
                raise Exception('Invalid value for separator: %r' % separator)
        else:
            separator = ','

        return ({'values': values, 'separator': separator},)
