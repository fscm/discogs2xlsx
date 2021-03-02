# -*- coding: UTF-8 -*-
#
# copyright: 2020-2021, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Logger module.

This module is based on the logging library.

The following is a simple usage example::
  from .logger import Logger
  l = Logger(level=Logger.Level.DEBUG)
  l.info('my log entry')

The module contains the following public classes:
  - Logger -- The main entry point for logging. As the example above
    shows, the Logger() class is used to take care of the logs.

All other classes in this module are considered implementation details.
"""

import logging
from enum import IntEnum, unique
from sys import stdout
from typing import Optional
from . import __project__


class Logger:
    """logger.

    This class uses the logging.Logger class to manage the logs.

    Args:
      level (Level, optional): Logging level. Defaults to Level.INFO.
      file (str, optional): Log file. Defaults to None.
    """

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

    def __init__(
            self,
            level: Optional[Level] = Level.INFO,
            file: Optional[str] = None):
        self.__file: str = file
        self.__level: Logger.Level = level
        self.__formatter: logging.Formatter = logging.Formatter(
            '[%(levelname)-8s] %(message)s')
        self.__console: logging.StreamHandler = logging.StreamHandler(
            self.__file or stdout)
        self.__console.setFormatter(self.__formatter)
        self.__logger: logging.Logger = logging.getLogger(f'{__project__}')
        self.__logger.setLevel(self.__level.value)
        self.__logger.addHandler(self.__console)

    @property
    def file(self) -> str:
        """str: log file option."""
        return self.__file

    @property
    def level(self) -> Level:
        """Level: log level option."""
        return self.__level

    def critical(self, msg: str) -> None:
        """Logs a 'msg % args' message with level 'CRITICAL' on this
        logger.

        Args:
          msg (str): Log message.
        """
        self.__logger.critical(msg)

    def debug(self, msg: str) -> None:
        """Logs a 'msg % args' message with level 'DEBUG' on this
        logger.

        Args:
          msg (str): Log message.
        """
        self.__logger.debug(msg)

    def error(self, msg: str) -> None:
        """Logs a 'msg % args' message with level 'ERROR' on this
        logger.

        Args:
          msg (str): Log message.
        """
        self.__logger.error(msg)

    def info(self, msg: str) -> None:
        """Logs a 'msg % args' message with level 'INFO' on this
        logger.

        Args:
          msg (str): Log message.
        """
        self.__logger.info(msg)

    def warning(self, msg: str) -> None:
        """Logs a 'msg % args' message with level 'WARNING' on this
        logger.

        Args:
          msg (str): Log message.
        """
        self.__logger.warning(msg)
