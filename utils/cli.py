# coding=utf-8
from argparse import ArgumentParser


class CLI:
    """ A CLI Based On argparse
        @command: used to command without arguments
        @option: used to command with arguments
        Don't mix this two decorators!
    """
    # Don't used this string as an argument
    SUBCOMMAND_MAGIC_FUNC = '__SUBCOMMAND_MAGIC_FUNC__'

    def __init__(self, 
                 prog,
                 version=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 add_help=True):
        settings = dict(
            prog=prog,
            usage=usage,
            description=description,
            epilog=epilog,
            add_help=add_help,
        )
        self.parser = ArgumentParser(**settings)
        if version:
            self.parser.add_argument('-v', '--version', 
                action='version',
                version='%(prog)s v{}'.format(version))
        self.subparsers = self.parser.add_subparsers(title='subcommands')
        self.subcommands = {}

    def command(self, **kwargs):
        def wrapper(_callable):
            title = kwargs.pop('title', None)
            description = kwargs.pop('description', None)
            if not title:
                title = _callable.__name__
            _parser = self.subparsers.add_parser(title, description=description)
            _parser.set_defaults(**{self.SUBCOMMAND_MAGIC_FUNC: _callable})
            self.subcommands[title] = _parser
            return _callable
        return wrapper

    def add_command(self, title, _callable, description=None):
        _parser = self.subparsers.add_parser(title, description=description)
        _parser.set_defaults(**{self.SUBCOMMAND_MAGIC_FUNC: _callable})
        self.subcommands[title] = _parser
        return self

    def option(self, *args, **kwargs):
        def wrapper(_callable):
            title = _callable.__name__
            _parser = self.subcommands.get(title, None)
            if not _parser:
                _parser = self.subparsers.add_parser(title)
            _parser.set_defaults(**{self.SUBCOMMAND_MAGIC_FUNC: _callable})
            _parser.add_argument(*args, **kwargs)
            self.subcommands[title] = _parser
            return _callable
        return wrapper

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)
        return self

    def run(self):
        namespace = self.parser.parse_args()
        args = namespace.__dict__
        callback = args.pop(self.SUBCOMMAND_MAGIC_FUNC, None)
        if callback:
            callback(**args)