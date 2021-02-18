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
from os import getcwd
from . import __project__, __version__


_default_file_collection = f'{getcwd()}/discogs-collection.xlsx'
_default_file_wantlist = f'{getcwd()}/discogs-wantlist.xlsx'


class _WantlistAction(argparse.Action):
    """Wantlist option action.

    This class extends argparse.Action to define the default file name
    for the wantlist option.

    Args:
      option_strings (str): The option string that was used to invoke
        this action.
      dest (str): The name of the attribute to be added to the object.
      default (bool): The value produced if the argument is absent from
        the command line and if it is absent from the namespace object.
      required (bool): Whether or not the command-line option may be
        omitted
      help (str): A brief description of what the argument does.
      metavar (str): A name for the argument in usage messages.
    """

    def __init__(
            self,
            option_strings,
            dest,
            default=False,
            required=False,
            help=None,  # pylint: disable=redefined-builtin
            metavar=None):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            const=True,
            default=default,
            required=required,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self.const)
        default_file = getattr(namespace, 'file')
        if default_file == _default_file_collection:
            try:
                default_file = _default_file_wantlist
            except TypeError:
                pass
            setattr(namespace, 'file', default_file)


class Options:
    """Command-line options parser.

    This class uses the argparse.ArgumentParser to parse and validate
    the command-line options.
    """

    __default_file = _default_file_collection

    def __init__(self):
        parser = argparse.ArgumentParser(
            prog=__project__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            add_help=True,
            allow_abbrev=False)
        mutually_exclusive = parser.add_mutually_exclusive_group(
            required=False)
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
            default=['EUR'],
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
            default=self.__default_file,
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
            # action='store_true',
            action=_WantlistAction,
            help='exports the wantlist instead of the collection')
        self.__options = parser.parse_args()

    @property
    def apikey(self):
        """str: apikey option."""
        return self.__options.apikey[0]

    @property
    def currency(self):
        """str: currency option."""
        return self.__options.currency[0]

    @property
    def debug(self):
        """bool: debug option."""
        return self.__options.debug

    @property
    def details(self):
        """bool: exports extra details option."""
        return self.__options.details

    @property
    def file(self):
        """str: data file option."""
        return self.__options.file

    @property
    def options(self):
        """dict: all options."""
        return {
            key: (
                value[0] if isinstance(
                    value,
                    list) else value) for (
                key,
                value) in vars(
                self.__options).items()}

    @property
    def prices(self):
        """bool: exports recommended prices option."""
        return self.__options.prices

    @property
    def quiet(self):
        """bool: quiet option."""
        return self.__options.quiet

    @property
    def wantlist(self):
        """bool: export wantlist instead of collection option."""
        return self.__options.wantlist
