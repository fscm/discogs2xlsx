# discogs2xlsx

Export your Discogs collection or wantlist into a xlsx file.

## Synopsis

This tool will try to export your collection or wantlist from Discogs into
a `.xlsx` file.

The time required to perform the export will depend on the size of your
collection, or wantlist.
Discogs requests to the API are throttled to 60 per minute for authenticated
requests, for that reason for large collections, or wantlists, the export can
take hours to perform.

## Prerequisites

There are a couple of things needed for the tool to work.

Python, version 3.6 or above, needs to be installed on your local computer.
You will also need a Discogs account.

### Discogs

A Discogs user account is required (to obtain the ratings from). You can
create an account at [https://www.discogs.com/users/create](https://www.discogs.com/users/create)
if you do not have one already.

A Discogs personal token is also required. You can obtain one at
[https://www.discogs.com/settings/developers](https://www.discogs.com/settings/developers)

For price recommendations (`--price` option) the
[Discogs Seller Settings](https://www.discogs.com/settings/seller/) are
required.

### Python 3.x

Python version 3.6 or above is required for the tool to work. Python setup can
be found [here](https://www.python.org/downloads/).

The following python modules are also required to run the tool:

* progress >= 1.5
* requests >= 2.25.1
* xlsxwriter >= 1.3.7

## Installation

The simplest way to install this tool is using pip:

```
pip3 install discogs2xlsx
```

## Usage

A simple example of how to use this tool:
```
discogs2xlsx -a my_discogs_secret_token
```

List of all the options:

```
usage: discogs2xlsx [-h] -a APIKEY [-c {AUD,BRL,CAD,CHF,EUR,GBP,JPY,MXN,NZD,SEK,USD,ZAR}] [--debug] [-d] [-f FILE] [-p] [-q] [-v] [-w]

optional arguments:
  -h, --help            show this help message and exit
  -a APIKEY, --apikey APIKEY
                        discogs api key (default: None)
  -c {AUD,BRL,CAD,CHF,EUR,GBP,JPY,MXN,NZD,SEK,USD,ZAR}, --currency {AUD,BRL,CAD,CHF,EUR,GBP,JPY,MXN,NZD,SEK,USD,ZAR}
                        currency for prices (default: 'EUR')
  --debug               debug mode (default: False)
  -d, --details         exports extra details (default: False)
  -f FILE, --file FILE  output file name (default:
                        /Users/fscm/Documents/Projects/Active/discogs2xlsx/discogs-collection.xlsx)
  -p, --prices          exports recommended prices (default: False)
  -q, --quiet           quiet mode (default: False)
  -v, --version         show program's version number and exit
  -w, --wantlist        exports the wantlist instead of the collection (default: False)
```

**IMPORTANT**
[Discogs Seller Settings](https://www.discogs.com/settings/seller/) are required
for the recommended prices option (`-p` `--prices`).

## Build (from source)

It is recommended the use of a Python Virtual Environment (venv) to build this
tool. The same Virtual Environment can also be used to run the tool.

All of the commands described bellow are to be executed on the root folder of
this project.

A Virtual Environment can be created using the follow command:

```
python3 -m venv venv/
```

After creating the Virtual Environment the same will have to be activated, run
the following command to do that:

```
source venv/bin/activate
```

To build and run the tool some Python modules are required. These modules can
be installed using the following command:

```
pip3 --quiet install --upgrade --requirement requirements.txt build
```

Finaly the Python package for this tool can be created with the command:

```
python3 -m build --wheel
```

After this you should endup with a wheel file (`*.whl`) inside a folder called
`dist`.

The tool can be install using the wheel file and pip3:

```
pip3 --quiet install dist/discogs2xlsx-*.whl
```

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

Please read the [CONTRIBUTING.md](https://github.com/fscm/discogs2xlsx/blob/master/CONTRIBUTING.md)
file for more details on how to contribute to this project.

## Versioning

This project uses [SemVer](http://semver.org/) for versioning. For the versions
available, see the [tags on this repository](https://github.com/fscm/discogs2xlsx/tags).

## Authors

* **Frederico Martins** - [fscm](https://github.com/fscm)

See also the list of [contributors](https://github.com/fscm/discogs2xlsx/contributors)
who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/fscm/discogs2xlsx/blob/master/LICENSE)
file for details
