# -*- coding: UTF-8 -*-
#
# copyright: 2020-2022, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Tests for the Options module."""

import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from os import environ
from pytest import raises
from . import __project__

MODULE = '_options'
options = __import__('{0}.{1}'.format(__project__, MODULE), fromlist=[''])


def test__options_fail_default():
    """test__options_fail_default

    Test if without any arguments given the 'required arguments' error
    is triggered.
    """
    with raises(SystemExit) as error:
        _ = options.Options(name=__project__, version='1.0.0')
    assert error.type == SystemExit
    assert error.value.code == 2


def test__options_fail_debug_quiet(mocker):
    """test__options_fail_debug_quiet

    Test if with the '--debug' and the '--quiet' arguments given the
    'not allowed' arguments error is triggered.

    Args:
        mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = [__project__, '--debug', '--quiet']
    mocker.patch.object(sys, 'argv', testargs)
    with raises(SystemExit) as wrapped_e:
        _ = options.Options(name=__project__, version='1.0.0')
    assert wrapped_e.type == SystemExit
    assert wrapped_e.value.code == 2


def test_logger_fail_change_immutable_properties(mocker):
    """test_logger_fail_change_immutable_properties.

    Args:
        mocker (pytest_mock.plugin.MockerFixture): Mocker.

    Test if Options immutable properties can be set/changed.
    """
    testargs = [__project__, '--token', 'dummy']
    mocker.patch.object(sys, 'argv', testargs)
    o = options.Options(name=__project__, version='1.0.0')
    with raises(AttributeError, match='can\'t set attribute'):
        o.all = {}


def test__options_fail_unrecognized(mocker):
    """test__options_fail_unrecognized

    Test if with an invalid argument given the 'unrecognized arguments'
    arguments error is triggered.

    Args:
        mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = [__project__, '--token', 'dummy', '--fake']
    mocker.patch.object(sys, 'argv', testargs)
    with raises(SystemExit) as error:
        _ = options.Options(name=__project__, version='1.0.0')
    assert error.type == SystemExit
    assert error.value.code == 2


def test__options_ok_all(mocker):
    """test__options_ok_all

    Test if 'all' was created.

    Args:
        mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = [__project__, '--token', 'dummy']
    mocker.patch.object(sys, 'argv', testargs)
    o = options.Options(name=__project__, version='1.0.0')
    assert o.all
    assert 'quiet' in o.all
    assert 'debug' in o.all


def test__options_ok_version(capsys, mocker):
    """test__options_ok_version

    Test if 'version' was created.

    Args:
        capsys (_pytest.capture.CaptureFixture): stdout, stderr,
            and stdin capture.
        mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = [__project__, '--version']
    mocker.patch.object(sys, 'argv', testargs)
    with raises(SystemExit) as error:
        _ = options.Options(name=__project__, version='1.0.0')
    captured = capsys.readouterr()
    assert captured.out == '1.0.0\n'
    assert captured.err == ''
    assert error.type == SystemExit
    assert error.value.code == 0


def test__options_ok_custom_parser(mocker):
    """test__options_ok_custom_parser

    Test Options with external parser.

    Args:
        mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = [__project__, '--token', 'dummy', '--quiet']
    mocker.patch.object(sys, 'argv', testargs)
    p = ArgumentParser(
        prog=__project__,
        formatter_class=ArgumentDefaultsHelpFormatter,
        add_help=True,
        allow_abbrev=False)
    o = options.Options(name=__project__, version='1.0.0', parser=p)
    assert o.all
    assert 'quiet' in o.all
    assert o.all['quiet']


def test__options_ok_env(mocker):
    """test__options_ok_env

    Test Options with environment variable.

    Args:
        mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = [__project__, '--token', 'dummy']
    mocker.patch.object(sys, 'argv', testargs)
    environ['TEST_VAR1'] = 'test_value1'
    p = ArgumentParser(
        prog=__project__,
        formatter_class=ArgumentDefaultsHelpFormatter,
        add_help=True,
        allow_abbrev=False)
    p.add_argument(
        '-t1',
        '--testvar1',
        action=options._EnvDefault,  # pylint: disable=protected-access
        nargs='?',
        env_var='TEST_VAR1',
        type=str,
        required=True,
        help=('Test environment variable 1.'))
    p.add_argument(
        '-t2',
        '--testvar2',
        action=options._EnvDefault,  # pylint: disable=protected-access
        nargs='?',
        default='default_test_value2',
        env_var='TEST_VAR2',
        type=str,
        required=False,
        help=('Test environment variable 2.'))
    o = options.Options(name=__project__, version='1.0.0', parser=p)
    assert o.all
    assert 'testvar1' in o.all
    assert o.all['testvar1'] == 'test_value1'
    assert 'testvar2' in o.all
    assert o.all['testvar2'] == 'default_test_value2'


def test__options_fail_env(mocker):
    """test__options_fail_env

    Test Options with environment variable.

    Args:
        mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = [__project__, '--token', 'dummy']
    mocker.patch.object(sys, 'argv', testargs)
    p = ArgumentParser(
        prog=__project__,
        formatter_class=ArgumentDefaultsHelpFormatter,
        add_help=True,
        allow_abbrev=False)
    with raises(
            ValueError,
            match='env_var is required for environment actions'):
        p.add_argument(
            '-t1',
            '--testvar1',
            action=options._EnvDefault,  # pylint: disable=protected-access
            nargs='?',
            env_var='',
            type=str,
            required=True,
            help=('Test environment variable 1.'))
    with raises(
            ValueError,
            match='env_var is required for environment actions'):
        p.add_argument(
            '-t2',
            '--testvar2',
            action=options._EnvDefault,  # pylint: disable=protected-access
            nargs='?',
            env_var=None,
            type=str,
            required=True,
            help=('Test environment variable 2.'))


def test__options_ok_default(mocker):
    """test__options_ok_default

    Test the default set of arguments. Mandatory options are provided
    to avoid validation errors.

    Args:
      mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = [__project__, '--token', 'dummy']
    mocker.patch.object(sys, 'argv', testargs)
    o = options.Options(name=__project__, version='1.0.0')
    default = {
        'currency': 'EUR',
        'debug': False,
        'details': False,
        'file': 'discogs-collection.xlsx',
        'prices': False,
        'quiet': False,
        'token': 'dummy',
        'wantlist': False}
    assert o.all == default


def test__options_ok_custom(mocker):
    """test__options_ok_custom

    Test changing the default set of arguments. Mandatory options are
    provided to avoid validation errors.

    Args:
      mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = [
        __project__,
        '--token', 'dummy',
        '--currency', 'USD',
        '--debug',
        '--details',
        '--file', 'custom.xlsx',
        '--prices',
        '--wantlist']
    mocker.patch.object(sys, 'argv', testargs)
    o = options.Options(name=__project__, version='1.0.0')
    custom = {
        'currency': 'USD',
        'debug': True,
        'details': True,
        'file': 'custom.xlsx',
        'prices': True,
        'quiet': False,
        'token': 'dummy',
        'wantlist': True}
    assert o.all == custom


def test__options_ok_duplicated_wantlistaction(mocker):
    """test__options_ok_duplicated_wantlistaction

    Test the usage of duplicated '--wantlist' argument and the custom
    'Action' assign to it.

    Args:
      mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = ['prog', '--token', 'dummy', '--wantlist', '--wantlist']
    mocker.patch.object(sys, 'argv', testargs)
    o = options.Options(name=__project__, version='1.0.0')
    assert o.all['wantlist']


def test__options_fail_wantlist(mocker):
    """test__options_fail_wantlist

    Test Options with wantlist action.

    Args:
        mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = [__project__, '--token', 'dummy']
    mocker.patch.object(sys, 'argv', testargs)
    p = ArgumentParser(
        prog=__project__,
        formatter_class=ArgumentDefaultsHelpFormatter,
        add_help=True,
        allow_abbrev=False)
    with raises(
            ValueError,
            match='target is required for wantlist actions'):
        p.add_argument(
            '-t1',
            '--testvar1',
            action=options._WantlistFile,  # pylint: disable=protected-access
            target='',
            help=('Test environment variable 1.'))
    with raises(
            ValueError,
            match='target is required for wantlist actions'):
        p.add_argument(
            '-t2',
            '--testvar2',
            action=options._WantlistFile,  # pylint: disable=protected-access
            target=None,
            help=('Test environment variable 2.'))
