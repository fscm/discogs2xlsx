# -*- coding: UTF-8 -*-
#
# copyright: 2020-2022, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Tests for the Options module."""

import sys
import pytest
from discogs2xlsx.options import Options


def test_options_fail_default():
    """test_options_fail_default

    Test if without any arguments given the 'required arguments' error
    is triggered.
    """
    with pytest.raises(SystemExit) as error:
        _ = Options()
    assert error.type == SystemExit
    assert error.value.code == 2


def test_options_fail_debug_quiet(mocker):
    """test_options_fail_debug_quiet

    Test if with the '--debug' and the '--quiet' arguments given the
    'not allowed' arguments error is triggered.

    Args:
      mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = ['prog', '--debug', '--quiet']
    mocker.patch.object(sys, 'argv', testargs)
    with pytest.raises(SystemExit) as wrapped_e:
        _ = Options()
    assert wrapped_e.type == SystemExit
    assert wrapped_e.value.code == 2


def test_options_fail_redefine_variable(mocker):
    """test_options_fail_redefine_variable

    Test if it is possible to assign a value to a 'read only'
    property from an Options instance.

    Args:
      mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = ['prog', '--apikey', 'dummy']
    mocker.patch.object(sys, 'argv', testargs)
    with pytest.raises(SyntaxError) as error:
        o = Options()
        o.apikey = 'SyntaxError'
    print(error)
    assert error.type == SyntaxError
    assert error.value.msg == 'cannot assign to operator'


def test_options_fail_unrecognized(mocker):
    """test_options_fail_unrecognized

    Test if with an invalid argument given the 'unrecognized arguments'
    arguments error is triggered.

    Args:
      mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = ['prog', '--apikey', 'dummy', '--fake']
    mocker.patch.object(sys, 'argv', testargs)
    with pytest.raises(SystemExit) as error:
        _ = Options()
    assert error.type == SystemExit
    assert error.value.code == 2


def test_options_ok_default(mocker):
    """test_options_ok_default

    Test the default set of arguments. '--apikey' is provided to avoid
    validation errors.

    Args:
      mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = ['prog', '--apikey', 'dummy']
    mocker.patch.object(sys, 'argv', testargs)
    o = Options()
    default = {
        'apikey': 'dummy',
        'currency': 'EUR',
        'debug': False,
        'details': False,
        'file': 'discogs-collection.xlsx',
        'prices': False,
        'quiet': False,
        'wantlist': False}
    assert o.all == default


def test_options_ok_duplicated_wantlistaction(mocker):
    """test_options_ok_duplicated_wantlistaction

    Test the usage of duplicated '--wantlist' argument and the custom
    'Action' assign to it.

    Args:
      mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = ['prog', '--apikey', 'dummy', '--wantlist', '--wantlist']
    mocker.patch.object(sys, 'argv', testargs)
    o = Options()
    assert o.all['wantlist']


def test_options_ok_custom(mocker):
    """test_options_ok_custom

    Test changing the default set of arguments. '--apikey' is provided
    to avoid validation errors.

    Args:
      mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = [
        'prog',
        '--apikey', 'dummy',
        '--currency', 'USD',
        '--debug',
        '--details',
        '--file', 'custom.xlsx',
        '--prices',
        '--wantlist']
    mocker.patch.object(sys, 'argv', testargs)
    o = Options()
    custom = {
        'apikey': 'dummy',
        'currency': 'USD',
        'debug': True,
        'details': True,
        'file': 'custom.xlsx',
        'prices': True,
        'quiet': False,
        'wantlist': True}
    assert o.all == custom
