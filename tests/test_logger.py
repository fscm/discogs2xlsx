# -*- coding: UTF-8 -*-
#
# copyright: 2020-2021, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Tests for the Logger module."""

from discogs2xlsx.logger import Logger


def test_logger_ok_default():
    """test_logger_ok_default

    Test if Logger default settings are set properly.
    """
    l = Logger()
    assert l.level == Logger.Level.INFO
    assert l.file is None


def test_logger_ok_level_output(caplog, capsys):
    """test_logger_ok_default

    Test if Logger methods work.

    Args:
      caplog (_pytest.logging.LogCaptureFixture): Log messages capture.
      capsys (_pytest.capture.CaptureFixture): stdout, stderr , and
        stdin capture.
    """
    caplog.set_level(Logger.Level.NONE)
    caplog.clear()
    l = Logger(level=Logger.Level.DEBUG)
    l.debug('_debug_')
    l.info('_info_')
    l.warning('_warning_')
    l.error('_error_')
    l.critical('_critical_')
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
    assert len(caplog.records) == 5
    assert caplog.records[0].message == '_debug_'
    assert caplog.records[1].message == '_info_'
    assert caplog.records[2].message == '_warning_'
    assert caplog.records[3].message == '_error_'
    assert caplog.records[4].message == '_critical_'
