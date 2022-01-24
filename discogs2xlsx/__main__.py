# -*- coding: UTF-8 -*-
#
# copyright: 2020-2022, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Discogs2Xlsx

This module exports you Discogs collection or wanlist into a xlsx
document.
"""

import sys
from . import __author__, __license__, __project__, __version__
from ._discogs import Discogs
from ._logger import Level, Logger
from ._options import Options
from ._xlsx import Xlsx


def main() -> None:
    """main method"""
    header = (
        f'{__project__} version {__version__}\n'
        f'by {__author__} under {__license__} license')
    options = Options(name=__project__, version=__version__)
    logger = Logger(
        name=__project__,
        **({'level': Level.NONE} if options.all['quiet'] else (
            {'level': Level.DEBUG} if options.all['debug'] else {})))
    if not options.all['quiet']:
        print(header)
    print(options.all)
    discogs = Discogs(
        token=options.all['apikey'],
        user_agent=f'{__project__} version {__version__}',
        currency=options.all['currency'],
        logger=logger)
    xlsx: Xlsx = Xlsx(
        author=__project__,
        comments=f'Created with {__project__} version {__version__}',
        logger=logger)
    to_file = options.all['file']
    if options.all['wantlist']:
        wantlist = discogs.get_wantlist(
            details=options.all['details'],
            prices=options.all['prices'])
        xlsx.save_wantlist(wantlist=wantlist, to_file=to_file)
    else:
        collection = discogs.get_collection(
            details=options.all['details'],
            prices=options.all['prices'])
        xlsx.save_collection(collection=collection, to_file=to_file)


if __name__ == '__main__':
    sys.exit(main())
