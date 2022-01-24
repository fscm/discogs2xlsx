# -*- coding: UTF-8 -*-
#
# copyright: 2020-2022, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Command-line parsing module.

This module is based on the `argparse` command-line parsing library.

The following is a simple usage example::

    >>> from ._options import Options
    >>> o = Options(name='my_prog', version='1.0.0')
    >>> for opt in o.all:
    ...     print(opt, o.all[opt], type(o.all[opt]))

The module contains the following public classes:
    - Options -- The main entry point for command-line parsing. As the
        example above shows, the Options() class is used to parse the
        arguments.

All other classes in this module are considered implementation details.
"""

from argparse import (
    Action,
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    Namespace)
from os import environ
from typing import Any, Optional
from . import DEFAULT_FILE_COLLECTION, DEFAULT_FILE_WANTLIST


__all__ = ['Options']


class _EnvDefault(Action):
    """Environment values action.

    This class extends `argparse.Action` to define the argument values
    from the Environment.

    Args:
        env_var (str): Name of the environment variable.
        required (bool, optionsl): If the argument is required. Defaults
            to True.
        default (Any, optional): Default argument value. Defaults to
            `None`.
        **kwargs: Arbitrary keyword arguments.
    """

    def __init__(
            self,
            env_var: str,
            required: Optional[bool] = False,
            default: Optional[Any] = None,
            **kwargs) -> None:
        if not env_var:
            raise ValueError('env_var is required for environment actions')
        default = environ.get(env_var, default)
        if required and default:
            required = False
        super().__init__(default=default, required=required, **kwargs)

    def __call__(
            self,
            parser: ArgumentParser,
            namespace: Namespace,
            values: list[str],
            option_string: Optional[str] = None) -> None:
        setattr(namespace, self.dest, values)  # pragma: no cover


class _WantlistFile(Action):
    """Wantlist option action.

    This class extends `argparse.Action` to define the default file name
    for the wantlist option.

    Args:
        target (str): Name of the file name variable to be changed.
        **kwargs: Arbitrary keyword arguments.
    """

    def __init__(
            self,
            target: str,
            **kwargs) -> None:
        if not target:
            raise ValueError('target is required for wantlist actions')
        self._target = target
        super().__init__(nargs=0, const=True, default=False, **kwargs)

    def __call__(
            self,
            parser: ArgumentParser,
            namespace: Namespace,
            values: list[str],
            option_string: Optional[str] = None) -> None:
        setattr(namespace, self.dest, self.const)
        if getattr(namespace, self._target) == DEFAULT_FILE_COLLECTION:
            setattr(namespace, self._target, DEFAULT_FILE_WANTLIST)


class Options:
    """Command-line options parser.

    Args:
        name (str): The Logger name.
        version (str): The version.
        parser (ArgumentParser, optional): Parser to be used instead of
            a new one. Defaults to `None`.

    This class uses the `argparse.ArgumentParser` to parse and validate
    the command-line options.
    """

    __slots__ = ('_all',)

    def __init__(
            self,
            name: str,
            version: str,
            parser: ArgumentParser = None) -> None:
        if parser is None:
            parser = ArgumentParser(
                prog=name,
                formatter_class=ArgumentDefaultsHelpFormatter,
                add_help=True,
                allow_abbrev=False)
        parser.register('action', 'environment', _EnvDefault)
        parser.register('action', 'wantlist', _WantlistFile)
        mutually_exclusive = \
            parser.add_mutually_exclusive_group(required=False)
        parser.add_argument(
            '-c',
            '--currency',
            action='store',
            nargs='?',
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
            nargs='?',
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
            '-t',
            '--token',
            action='environment',
            nargs='?',
            env_var='DISCOGS_TOKEN',
            type=str,
            required=True,
            help=(
                'discogs token (can also be set usibg the DISCOGS_TOKEN '
                'environment variable)'))
        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=version)
        parser.add_argument(
            '-w',
            '--wantlist',
            action='wantlist',
            target='file',
            help='exports the wantlist instead of the collection')
        self._all = vars(parser.parse_args())

    @property
    def all(self) -> dict[str, Any]:
        """Dict: all options."""
        return self._all
