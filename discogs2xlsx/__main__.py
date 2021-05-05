# -*- coding: UTF-8 -*-
#
# copyright: 2020-2021, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Discogs2Xlsx

This module exports you Discogs collection or wanlist into a xlsx
document.
"""

import sys
from . import __author__, __license__, __project__, __version__
from .discogs import Discogs
from .logger import Logger
from .options import Options
from .xlsx import Xlsx


def main() -> None:
    """main method"""
    header = (
        f'{__project__} version {__version__}\n'
        f'by {__author__} under {__license__} license')
    options = Options()
    # pylint: disable=repeated-keyword
    logger = Logger(
        **({'level': Logger.Level.NONE} if options.all['quiet'] else {}),
        **({'level': Logger.Level.DEBUG} if options.all['debug'] else {}))
    # pylint: enable=repeated-keyword
    if not options.all['quiet']:
        print(header)
    discogs = Discogs(
        key=options.all['apikey'],
        currency=options.all['currency'],
        logger=logger)
    xlsx: Xlsx = Xlsx(logger=logger)
    if options.all['wantlist']:
        wantlist = discogs.get_wantlist(
            details=options.all['details'],
            prices=options.all['prices'])
        xlsx.save_wantlist(wantlist=wantlist, to_file=options.all['file'])
    else:
        collection = discogs.get_collection(
            details=options.all['details'],
            prices=options.all['prices'])
        xlsx.save_collection(
            collection=collection,
            to_file=options.all['file'])


if __name__ == '__main__':
    sys.exit(main())
