# -*- coding: UTF-8 -*-
#
# copyright: 2020-2022, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Logger module.

This module is based on the `logging` library.

The following is a simple usage example::

    >>> from ._logger import Logger, Level
    >>> l = Logger(name='my_prog', level=Level.DEBUG)
    >>> l.info('my log entry')

This module can also be used to write the messages to the screen and a
file simultaneously::

    >>> from ._logger import Logger, Level
    >>> l = Logger(name='my_prog', level=Level.DEBUG)
    >>> l = Logger(name='my_prog', file='my_app.log', color=False)
    >>> l.info('my log entry on both screen and file')

The module contains the following public classes:

* Level -- An enumerator with the `Logger` levels.
* Logger -- The main entry point for logging. As the example above
    shows, the Logger() class is used to take care of the logs.

All other classes in this module are considered implementation details.
"""

import logging
from enum import IntEnum, unique
from sys import stderr, stdout
from typing import Optional

try:
    import curses
except ImportError:
    curses = None


__all__ = [
    'Level',
    'Logger']


@unique
class Level(IntEnum):
    """Logger verbosity levels.

    Args:
        Enum (int): Verbosiy level.
    """
    DEBUG: int = logging.DEBUG
    INFO: int = logging.INFO
    WARNING: int = logging.WARNING
    ERROR: int = logging.ERROR
    CRITICAL: int = logging.CRITICAL
    NONE: int = logging.NOTSET


class _Color(IntEnum):
    """Logger colors.

    Args:
        Enum (int): Color.
    """
    DEBUG: int = 7     # white
    INFO: int = 2      # green
    WARNING: int = 3   # yellow
    ERROR: int = 1     # red
    CRITICAL: int = 1  # red


def _terminal_has_colors() -> bool:
    """Initialize the terminal and check if it support colors.

    Returns:
        bool: True if successful False otherwise.
    """
    if not (hasattr(stderr, 'isatty') and stderr.isatty()):
        return False
    try:
        curses.setupterm()
        return curses.tigetnum('colors') > 0
    except Exception:  # pylint: disable=broad-except
        return False


class _LogFormatter(logging.Formatter):
    """LogFormatter.

    Log formatter to use for color support.

    Args:
        color (bool, optional): Use Colors. Defaults to True.
    """

    __slots__ = (
        '_color',
        '_colors',
        '_normal')

    def __init__(self, color: Optional[bool] = True) -> None:
        super().__init__(fmt=None)
        self._colors = {}
        if color and _terminal_has_colors():
            fg = (curses.tigetstr('setaf') or curses.tigetstr('setf') or '')
            for name, value in _Color.__members__.items():
                self._colors[Level[name].value] = str(
                    curses.tparm(fg, value.value), 'ascii')
            self._normal = str(curses.tigetstr('sgr0'), 'ascii')
        else:
            self._normal = ''

    def formatMessage(self, record: logging.LogRecord) -> str:
        """Format a message from a record object.

        Args:
            record (logging.LogRecord): Use Colors. Defaults to True.

        Returns:
            str: The formated message.
        """
        if record.levelno in self._colors:
            start_color = self._colors[record.levelno]
            end_color = self._normal
        else:
            start_color = end_color = ''
        return (
            f'{start_color}[{record.levelname:<8}] '
            f'{record.message}{end_color}')


class Logger:
    """logger.

    This class uses the `logging.Logger` class to manage the logs.

    Args:
        name (str): The Logger name.
        level (Level, optional): Logging level. Defaults to Level.INFO.
        file (str, optional): Log file. Defaults to None.
        color (bool, optional): Use Colors. Defaults to True.
    """

    __slots__ = (
        '_console',
        '_file',
        '_level',
        '_logger',
        '_name')

    def __init__(
            self,
            name: str,
            level: Optional[Level] = Level.INFO,
            file: Optional[str] = None,
            color: Optional[bool] = True) -> None:
        self._name = name
        self._file = file
        self._level = level
        if self._file:
            self._console = logging.FileHandler(
                filename=file,
                mode='a',
                delay=True)
        else:
            self._console = logging.StreamHandler(stdout)
        self._console.setFormatter(_LogFormatter(color=color))
        self._logger = logging.getLogger(self._name)
        self._logger.setLevel(self._level.value)
        self._logger.addHandler(self._console)

    @property
    def file(self) -> str:
        """str: log file option."""
        return self._file

    @property
    def handlers(self) -> list[logging.Handler]:
        """list[logging.Handler]: log handlers."""
        return self._logger.handlers

    @property
    def level(self) -> Level:
        """Level: log level option."""
        return self._level

    @level.setter
    def level(self, level) -> None:
        self._level = level
        self._logger.setLevel(self._level.value)

    @property
    def name(self) -> str:
        """name: log name option."""
        return self._name

    def critical(self, msg: str) -> None:
        """Logs a 'msg % args' message with level 'CRITICAL' on this
        logger.

        Args:
            msg (str): Log message.
        """
        self._logger.critical(msg)

    def debug(self, msg: str) -> None:
        """Logs a 'msg % args' message with level 'DEBUG' on this
        logger.

        Args:
            msg (str): Log message.
        """
        self._logger.debug(msg)

    def error(self, msg: str) -> None:
        """Logs a 'msg % args' message with level 'ERROR' on this
        logger.

        Args:
            msg (str): Log message.
        """
        self._logger.error(msg)

    def info(self, msg: str) -> None:
        """Logs a 'msg % args' message with level 'INFO' on this
        logger.

        Args:
            msg (str): Log message.
        """
        self._logger.info(msg)

    def warning(self, msg: str) -> None:
        """Logs a 'msg % args' message with level 'WARNING' on this
        logger.

        Args:
            msg (str): Log message.
        """
        self._logger.warning(msg)

    def remove_handler(self, handler: logging.Handler) -> None:
        """Removes the specified handler from this logger.

        Args:
            msg (logging.Handler): The handler to be removed.

        """
        self._logger.removeHandler(handler)


del IntEnum, unique
