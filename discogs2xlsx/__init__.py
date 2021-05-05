# -*- coding: UTF-8 -*-
#
# copyright: 2020-2021, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""discogs2xlsx.

Export your Discogs collection or wantlist into a xlsx file.

This tool will try to export your collection or wantlist from Discogs
into a `.xlsx` file.

.. note::
    The time required to perform the export will depend on the size of
    your collection, or wantlist.
    Discogs requests to the API are throttled to 60 per minute for
    authenticated requests, for that reason for large collections, or
    wantlists, the export can take hours to perform.

A simple example of how to use this tool::

    discogs2xlsx -a my_discogs_secret_token
"""

from typing import Final

__author__: Final[str] = 'Frederico Martins'
__license__: Final[str] = 'MIT'
__project__: Final[str] = __package__
__version__: Final[str] = '0.3.0'

DEFAULT_FILE_COLLECTION: Final[str] = 'discogs-collection.xlsx'
DEFAULT_FILE_WANTLIST: Final[str] = 'discogs-wantlist.xlsx'
