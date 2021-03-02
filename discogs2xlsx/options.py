# -*- coding: UTF-8 -*-
#
# copyright: 2020-2021, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Command-line parsing module.

This module is based on the argparse command-line parsing library.

The following is a simple usage example::
  from .options import Options
  o = Options()
  for opt in o.options:
      print(opt, o.options[opt], type(o.options[opt]))

The module contains the following public classes:
  - Options -- The main entry point for command-line parsing. As the
    example above shows, the Options() class is used to parse the
    arguments.

All other classes in this module are considered implementation details.
"""

import argparse
from typing import Any, Optional
from . import __project__, __version__
from . import DEFAULT_FILE_COLLECTION, DEFAULT_FILE_WANTLIST

# type aliases
ArgumentParser = argparse.ArgumentParser
MutuallyExclusiveGroup = (
    argparse._MutuallyExclusiveGroup) # pylint: disable=protected-access
Namespace = argparse.Namespace


class _WantlistAction(argparse.Action):
    """Wantlist option action.

    This class extends argparse.Action to define the default file name
    for the wantlist option.
    """

    def __call__(
            self,
            parser: ArgumentParser,
            namespace: Namespace,
            values: list[str],
            option_string: Optional[str] = None) -> None:
        setattr(namespace, self.dest, self.const)
        if getattr(namespace, 'file') == DEFAULT_FILE_COLLECTION:
            setattr(namespace, 'file', DEFAULT_FILE_WANTLIST)


class Options:
    """Command-line options parser.

    This class uses the argparse.ArgumentParser to parse and validate
    the command-line options.
    """

    def __init__(self) -> None:
        parser: ArgumentParser = argparse.ArgumentParser(
            prog=__project__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            add_help=True,
            allow_abbrev=False)
        mutually_exclusive: MutuallyExclusiveGroup = \
            parser.add_mutually_exclusive_group(required=False)
        parser.add_argument(
            '-a',
            '--apikey',
            action='store',
            nargs=1,
            type=str,
            required=True,
            help='discogs api key')
        parser.add_argument(
            '-c',
            '--currency',
            action='store',
            nargs=1,
            default='EUR',
            type=str,
            choices=[
                'AUD',
                'BRL',
                'CAD',
                'CHF',
                'EUR',
                'GBP',
                'JPY',
                'MXN',
                'NZD',
                'SEK',
                'USD',
                'ZAR'],
            help='currency for prices')
        mutually_exclusive.add_argument(
            '--debug',
            action='store_true',
            help='debug mode')
        parser.add_argument(
            '-d',
            '--details',
            action='store_true',
            help='exports extra details')
        parser.add_argument(
            '-f',
            '--file',
            action='store',
            nargs=1,
            default=DEFAULT_FILE_COLLECTION,
            type=str,
            help='output file name')
        parser.add_argument(
            '-p',
            '--prices',
            action='store_true',
            help='exports recommended prices')
        mutually_exclusive.add_argument(
            '-q',
            '--quiet',
            action='store_true',
            help='quiet mode')
        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=__version__)
        parser.add_argument(
            '-w',
            '--wantlist',
            action=_WantlistAction,
            nargs=0,
            const=True,
            default=False,
            help='exports the wantlist instead of the collection')
        self.__args: dict[str, Any] = parser.parse_args()
        self.__all: dict[str, Any] = {
            k: (v[0] if isinstance(v, list) and not isinstance(
                v, str) else v) for (k, v) in vars(self.__args).items()}
        for k, v in self.__all.items():
            setattr(self, k, v)

    def __setattr__(self, name: Any, value: Any) -> None:
        if name in self.__dict__:
            raise SyntaxError('cannot assign to operator')
            #raise AttributeError('cannot assign to operator')
        self.__dict__[name] = value

    @property
    def all(self) -> dict[str, Any]:
        """dict: all options."""
        return self.__all
