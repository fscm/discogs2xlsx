# -*- coding: UTF-8 -*-
#
# copyright: 2020-2022, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Tests for the module entry point."""

import sys
import pytest
from discogs2xlsx.__main__ import main


def test___main___fail(mocker):
    """test___main___fail

    Test if program exits with error.

    Args:
      mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = ['prog', '--fake']
    mocker.patch.object(sys, 'argv', testargs)
    with pytest.raises(SystemExit) as wrapped_e:
        main()
    assert wrapped_e.type == SystemExit
    assert wrapped_e.value.code == 2


def test___main___ok(mocker):
    """test_options_fail_debug_quiet

    Test if program executes properly.

    Args:
      mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    testargs = ['prog', '--version']
    mocker.patch.object(sys, 'argv', testargs)
    with pytest.raises(SystemExit) as wrapped_e:
        main()
    assert wrapped_e.type == SystemExit
    assert wrapped_e.value.code == 0
