# -*- coding: UTF-8 -*-
#
# copyright: 2020-2022, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Tests for the Logger module."""

from curses import setupterm, tigetnum
from pytest import raises
from . import __project__

MODULE = '_logger'
logger = __import__('{0}.{1}'.format(__project__, MODULE), fromlist=[''])


def _clear_logger(lggr: logger.Logger) -> None:
    """Removes the logger handlers.

    Args:
        lggr (logger.Logger): The logger.
    """
    for handler in lggr.handlers[:]:
        lggr.remove_handler(handler)


def _fake_fail_setupterm() -> None:
    """Simulates setupterm failing with the Exception exception.

    Raises:
        Exception: Always :)

    """
    raise Exception('Sorry, this is supposed to fail.')


def _fake_terminal_has_colors() -> bool:
    """Initialize the terminal as one that supports colors.

    Returns:
        bool: True if successful False otherwise.
    """
    try:
        setupterm(term='xterm-256color', fd=1)
        return tigetnum('colors') > 0
    except Exception:  # pylint: disable=broad-except
        return False


def test__logger_ok_default():
    """test__logger_ok_default.

    Test if Logger default settings are set properly.
    """
    l = logger.Logger(name=__project__)
    _clear_logger(l)
    assert l.level == logger.Level.INFO
    assert l.file is None


def test__logger_ok_file():
    """test__logger_ok_file.

    Test if Logger properties were set with the right values.
    """
    file_name = '{0}.log'.format(__project__)
    l = logger.Logger(
        name=__project__,
        level=logger.Level.DEBUG,
        file=file_name,
        color=False)
    _clear_logger(l)
    assert l.file is file_name
    assert l.level == logger.Level.DEBUG
    assert l.name == __project__


def test__logger_ok_change_mutable_properties():
    """test__logger_ok_change_mutable_properties.

    Test if Logger mutable properties (level) can be set/changed.
    """
    l = logger.Logger(name=__project__, level=logger.Level.DEBUG)
    l.level = logger.Level.WARNING
    _clear_logger(l)
    assert l.level == logger.Level.WARNING


def test__logger_fail_change_immutable_properties():
    """test__logger_fail_change_immutable_properties.

    Test if Logger immutable properties can be set/changed.
    """
    l = logger.Logger(name=__project__, level=logger.Level.DEBUG)
    _clear_logger(l)
    with raises(AttributeError, match='can\'t set attribute'):
        l.name = 'new_name'
    with raises(AttributeError, match='can\'t set attribute'):
        l.file = 'new_log_file.log'


def test__logger_ok_level_output(caplog, capsys):
    """test__logger_ok_default

    Test if Logger methods work.

    Args:
        caplog (_pytest.logging.LogCaptureFixture): Log messages
            capture.
        capsys (_pytest.capture.CaptureFixture): stdout, stderr,
            and stdin capture.
    """
    caplog.set_level(logger.Level.NONE)
    caplog.clear()
    l = logger.Logger(name=__project__, level=logger.Level.DEBUG, color=False)
    l.debug('_debug_')
    l.info('_info_')
    l.warning('_warning_')
    l.error('_error_')
    l.critical('_critical_')
    _clear_logger(l)
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
    assert len(caplog.records) == 5
    assert caplog.records[0].message == '_debug_'
    assert caplog.records[1].message == '_info_'
    assert caplog.records[2].message == '_warning_'
    assert caplog.records[3].message == '_error_'
    assert caplog.records[4].message == '_critical_'


def test__logger_ok__terminal_has_colors(mocker):
    """test__logger_ok__terminal_has_colors

    Test if terminal support colors.

    Args:
        mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    mocker.patch(
        '{0}.{1}.stderr.isatty'.format(
            __project__, MODULE), return_value=True)
    mocker.patch(
        '{0}.{1}.curses.setupterm'.format(
            __project__, MODULE), return_value=None)
    mocker.patch(
        '{0}.{1}.curses.tigetnum'.format(
            __project__, MODULE), return_value=256)
    assert logger._terminal_has_colors()  # pylint: disable=protected-access


def test__logger_fail__terminal_has_colors(mocker):
    """test__logger_fail__terminal_has_colors

    Test if terminal support colors.

    Args:
      mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    mocker.patch(
        '{0}.{1}.stderr.isatty'.format(
            __project__, MODULE), return_value=True)
    mocker.patch(
        '{0}.{1}.curses.setupterm'.format(__project__, MODULE),
        new=_fake_fail_setupterm)
    assert not logger._terminal_has_colors()  # pylint: disable=protected-access


def test__logger_ok_colors(caplog, capsys, mocker):
    """test__logger_ok_colors

    Test colors support.

    Args:
        caplog (_pytest.logging.LogCaptureFixture): Log messages
            capture.
        capsys (_pytest.capture.CaptureFixture): stdout, stderr,
            and stdin capture.
        mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    mocker.patch(
        '{0}.{1}._terminal_has_colors'.format(__project__, MODULE),
        new=_fake_terminal_has_colors)
    caplog.set_level(logger.Level.NONE)
    caplog.clear()
    l = logger.Logger(name=__project__, level=logger.Level.DEBUG, color=True)
    l.debug('_debug_')
    l.info('_info_')
    l.warning('_warning_')
    l.error('_error_')
    l.critical('_critical_')
    _clear_logger(l)
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
    assert len(caplog.records) == 5
    assert caplog.records[0].message == '_debug_'
    assert caplog.records[1].message == '_info_'
    assert caplog.records[2].message == '_warning_'
    assert caplog.records[3].message == '_error_'
    assert caplog.records[4].message == '_critical_'
