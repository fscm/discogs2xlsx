# -*- coding: UTF-8 -*-
#
# copyright: 2020-2021, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Exports your Discogs collection or wantlist into a xlsx file."""

import sys
from .discogs2xlsx import main


if __name__ == '__main__':
    sys.exit(main())
