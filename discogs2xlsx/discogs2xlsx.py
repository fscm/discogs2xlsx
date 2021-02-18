# -*- coding: UTF-8 -*-
#
# copyright: 2020-2021, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Discogs2Xlsx

This module exports you Discogs collection or wanlist into a xlsx
document.

The following is a simple usage example::
  d2x = Discogs2Xlsx()
  d2x.main()

The module contains the following public classes:
  - Discogs2Xlsx -- The main entry point. As the example above shows,
    the Discogs2Xlsx() class can be used to start the application that
    will export your collection or wantlist.

All other classes in this module are considered implementation details.
"""

from . import __author__, __license__, __project__, __version__
from .discogs import Discogs
from .logger import Logger
from .options import Options
from .xlsx import Xlsx


class Discogs2Xlsx:
    """Exports your Discogs collection or wantlist into a xlsx file."""

    __header: str = (
        f'{__project__} version {__version__}\n'
        f'by {__author__} under {__license__} license')

    def main(self) -> None:
        """main method"""
        options = Options()
        # pylint: disable=repeated-keyword
        logger = Logger(
            **({'level': Logger.Level.NONE} if options.quiet else {}),
            **({'level': Logger.Level.DEBUG} if options.debug else {}))
        # pylint: enable=repeated-keyword
        if not options.quiet:
            print(self.__header)
        discogs = Discogs(
            key=options.apikey,
            currency=options.currency,
            logger=logger)
        xlsx = Xlsx(logger=logger)
        if options.wantlist:
            wantlist = discogs.get_wantlist(
                details=options.details,
                prices=options.prices)
            xlsx.save_wantlist(wantlist=wantlist, to_file=options.file)
        else:
            collection = discogs.get_collection(
                details=options.details,
                prices=options.prices)
            xlsx.save_collection(collection=collection, to_file=options.file)


def main() -> None:
    d2x = Discogs2Xlsx()
    d2x.main()
