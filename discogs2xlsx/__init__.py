# -*- coding: UTF-8 -*-
#
# copyright: 2020-2022, Frederico Martins
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

## Prerequisites

There are a couple of things needed for the tool to work.

Python, version 3.9 or above, needs to be installed on your local
computer. You will also need a Discogs account.

### Discogs

A Discogs user account is required (to obtain the ratings from). You can
create an account at [discogs.com](https://www.discogs.com/users/create)
if you do not have one already.

A Discogs personal token is also required. You can obtain one at
[discogs.com](https://www.discogs.com/settings/developers)

For price recommendations (`--prices` option) the
[Discogs Seller Settings](https://www.discogs.com/settings/seller/) are
required.

### Python 3.x

Python version 3.9 or above is required for the tool to work. Python
setup can be found [here](https://www.python.org/downloads/).

The following python modules are also required to run the tool:

* progress >= 1.5
* requests >= 2.25.1
* xlsxwriter >= 3.0.0

## Installation

The simplest way to install this tool is using pip:

```shell
pip3 install discogs2xlsx
```

## Usage

A simple example of how to use this tool:

```shell
discogs2xlsx --token my_discogs_secret_token
```

List of all the options:

```shell
usage: discogs2xlsx [-h] [-c [{AUD,BRL,CAD,CHF,EUR,GBP,JPY,MXN,NZD,SEK,USD,ZAR}]] [--debug] [-d] [-f [FILE]] [-p] [-q]
                    -t [TOKEN] [-v] [-w]

options:
  -h, --help            show this help message and exit
  -c [{AUD,BRL,CAD,CHF,EUR,GBP,JPY,MXN,NZD,SEK,USD,ZAR}], --currency [{AUD,BRL,CAD,CHF,EUR,GBP,JPY,MXN,NZD,SEK,USD,ZAR}]
                        currency for prices (default: EUR)
  --debug               debug mode (default: False)
  -d, --details         exports extra details (default: False)
  -f [FILE], --file [FILE]
                        output file name (default: discogs-collection.xlsx)
  -p, --prices          exports recommended prices (default: False)
  -q, --quiet           quiet mode (default: False)
  -t [TOKEN], --token [TOKEN]
                        discogs token (can also be set usibg the DISCOGS_TOKEN environment variable) (default: None)
  -v, --version         show program's version number and exit
  -w, --wantlist        exports the wantlist instead of the collection (default: False)
```

.. important::
    [Discogs Seller Settings](https://www.discogs.com/settings/seller/)
    are required for the recommended prices option (`-p` `--prices`).
"""

from typing import Final


__all__ = []


__author__: Final[str] = 'Frederico Martins'
__license__: Final[str] = 'MIT'
__project__: Final[str] = __package__
__version__: Final[str] = '0.4.0'

DEFAULT_FILE_COLLECTION: Final[str] = 'discogs-collection.xlsx'
DEFAULT_FILE_WANTLIST: Final[str] = 'discogs-wantlist.xlsx'
