# -*- coding: UTF-8 -*-
#
# copyright: 2020-2021, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Discogs data handler.

This module handles Discogs data.

The following is a simple usage example::

    >>> from .discogs import Discogs
    >>> d = Discogs('my_discogs_secret_token')
    >>> c = discogs.get_collection()
    >>> print(c)

The module contains the following public classes:
    - Discogs -- Data handler. As the example above shows, the Discogs()
        class can be used to load data from Discogs.
    - DiscogsException -- Generic Discogs API exception.

All other classes in this module are considered implementation details.
"""

import sys
from json import loads
from re import sub
from time import time, sleep
from typing import Any, Final, Optional
from progress.bar import Bar
from requests import sessions
from . import __project__


class DiscogsException(Exception):
    """Generic Discogs API exception."""


class Discogs:
    """Data handler.

    This class loads data from Discogs.

    Args:
        key (str): Discogs API key.
        currency (str, optional): Currency for prices (one of 'AUD'
            'BRL' 'CAD' 'CHF' 'EUR' 'GBP' 'JPY' 'MXN' 'NZD' 'SEK' 'USD'
            'ZAR'). Defaults to 'EUR'.
        logger (logger.Logger, optional): Logger to use. Defaults to
            None.
    """

    class DiscogsRequests():
        """Requests Handler.

        This class will handle the requests made to the discogs API.

        Args:
            key (str): Discogs API key.
        """

        API_BASEURL: Final[str] = 'https://api.discogs.com'
        API_FORMAT: Final[str] = 'application/vnd.discogs.v2.plaintext+json'
        API_LIMIT: Final[int] = 100
        API_RATELIMIT: Final[int] = 60
        API_RATELIMIT_STATUS: Final[int] = 429
        API_RATELIMIT_TIME: Final[int] = 60
        API_UNAUTHORIZED_STATUS: Final[int] = 401

        def __init__(self, key: str) -> None:
            self.__key = key
            self.__api_last_block_time = time()
            self.__headers = {
                'Accept': self.API_FORMAT,
                'Accept-Encoding': 'gzip',
                'Content-Type': 'application/json',
                'User-Agent': __project__}
            self.__params = {
                'token': f'{self.__key}',
                'per_page': self.API_LIMIT}
            self.__remaining_queries = self.API_RATELIMIT
            self.__session = sessions.Session()

        def request(
                self,
                path: str,
                params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
            """Method to perform a request to the Discogs API.

            Args:
                path (str): Request URL path.
                params (dict[str, Any], optional): Extra requests params.
                    Defaults to None.

            Returns:
                dict[str, Any]: Discogs API data.

            Raises:
                DiscogsException: If `key` is invalid.
            """
            if self.__remaining_queries < 2:
                now = time()
                sleep(max(2, self.API_RATELIMIT_TIME - (
                    now - self.__api_last_block_time)))
                self.__api_last_block_time = now
            response = self.__session.get(
                f'{self.API_BASEURL}{path}',
                params={
                    **self.__params,
                    **params} if params else self.__params,
                headers=self.__headers)
            headers = response.headers
            status_code = response.status_code
            self.__remaining_queries = int(
                headers.get(
                    'X-Discogs-Ratelimit-Remaining',
                    self.API_RATELIMIT))
            if status_code == self.API_UNAUTHORIZED_STATUS:
                raise DiscogsException('Unauthorized request.')
            if status_code == self.API_RATELIMIT_STATUS:
                self.__remaining_queries = 0
                return self.request(path=path, params=params)
            return loads(response.content)

    def __init__(
            self,
            key: str,
            currency: Optional[str] = 'EUR',
            logger: Optional['Logger'] = None) -> None:
        self.__requests = self.DiscogsRequests(key)
        self.__currency = currency
        self.__logger = logger
        try:
            self.__identity = self.__requests.request(path='/oauth/identity')
            self.__username = self.__identity['username']
        except DiscogsException as de:
            if self.__logger:
                self.__logger.error('Invalid Discogs key.')
                self.__logger.debug(de)
            sys.exit(1)

    def __get_discogs_data(
            self,
            pages: int,
            releases_path: str,
            label: str = 'Data',
            details: Optional[bool] = False,
            prices: Optional[bool] = False) -> dict[str, Any]:
        """Private method to help obtaining discogs data from the
        collection and/or wantlist.

        Args:
            pages (int): Number of pages to fetch.
            releases_path (str): Path of the desired data.
            label (str, optional): Label for the progress bar. Defaults
                to 'Data'.
            details (bool, optional): Export extra details for each
                collection item. Defaults to False.
            prices (bool, optional): Export the recommended prices for
                each collection item. Defaults to False.

        Returns:
            dict[str, Any]: Data.
        """
        data = {}
        request = self.__requests.request
        try:
            for page in Bar(f'{label:10}').iter(range(1, pages)):
                content = request(path=releases_path, params={'page': page})
                releases = content.get('releases') or content.get('wants')
                for release in releases:
                    r_id = release['id']
                    r_instance_id = release.get('instance_id', r_id)
                    r_artist = ' - '.join(map(
                        lambda x: sub(r'\(\d+\)', '', x['name']).strip(),
                        release['basic_information']['artists'])).title()
                    r_url = release['basic_information']['resource_url']
                    data.setdefault(r_artist, {})
                    data[r_artist].setdefault(r_instance_id, {})
                    data[r_artist][r_instance_id].setdefault(
                        'album', release['basic_information']['title'].title())
                    data[r_artist][r_instance_id].setdefault(
                        'year', int(release['basic_information']['year']))
                    data[r_artist][r_instance_id].setdefault('id', r_id)
                    t = [(f['name'].strip().upper(), int(f['qty']))
                         for f in release['basic_information']['formats']]
                    r_fmt_qty = {x: 0 for x, _ in t}
                    for k, v in t:
                        r_fmt_qty[k] += v
                    data[r_artist][r_instance_id].setdefault(
                        'format', ' - '.join(r_fmt_qty.keys()))
                    data[r_artist][r_instance_id].setdefault(
                        'quantity', ' - '.join(map(str, r_fmt_qty.values())))
                    data[r_artist][r_instance_id].setdefault(
                        'instance_id', r_instance_id)
                    data[r_artist][r_instance_id].setdefault(
                        'catno',
                        ' - '.join(map(
                            lambda x: x['catno'].strip(),
                            release['basic_information']['labels'])).upper())
                    data[r_artist][r_instance_id].setdefault(
                        'styles',
                        ', '.join(map(
                            lambda x: x.strip(),
                            release['basic_information']['styles'])).title())
                    data[r_artist][r_instance_id].setdefault(
                        'url', r_url)
            if details or prices:
                records = [(b, a, data[b][a]['id']) for b, a in [
                    i for s in map(
                        lambda x: [(x, b) for b in data[x].keys()],
                        data.keys()) for i in s]]
            if details:
                for artist, instance_id, r_id in Bar('Details').iter(records):
                    r_details = request(
                        path=f'/releases/{r_id}',
                        params={'curr_abbr': self.__currency})
                    r_details_community = r_details.get('community', {})
                    data[artist][instance_id].setdefault(
                        'have', int(r_details_community.get('have', 0)))
                    data[artist][instance_id].setdefault(
                        'want', int(r_details_community.get('want', 0)))
                    data[artist][instance_id].setdefault(
                        'uri', r_details.get('uri', ''))
                    data[artist][instance_id].setdefault(
                        'notes', r_details.get('notes', ''))
                    data[artist][instance_id].setdefault(
                        'num_for_sale', int(r_details.get('num_for_sale', 0)))
                    data[artist][instance_id].setdefault(
                        'lowest_price',
                        '{:,.2f}'.format(
                            r_details.get('lowest_price', 0) or 0))
            if prices:
                for artist, instance_id, r_id in Bar('Prices').iter(records):
                    r_prices = request(
                        path=f'/marketplace/price_suggestions/{r_id}')
                    data[artist][instance_id].setdefault(
                        'prices',
                        {sub(r' \(.*\)', '', key).lower().replace(
                            ' ', '_'): '{:,.2f}'.format(
                                r_prices[key]['value'])
                            for key in r_prices.keys()})
        except DiscogsException as de:
            if self.__logger:
                self.__logger.error('Fetching Discogs collection failled.')
                self.__logger.debug(de)
        except Exception as e:  # pylint: disable=broad-except
            if self.__logger:
                self.__logger.error('Unable to get Discogs data.')
                self.__logger.debug(e)
        return data

    def get_collection(
            self,
            details: Optional[bool] = False,
            prices: Optional[bool] = False) -> dict[str, Any]:
        """Fetch Discogs albums from the user's collection.

        Args:
            details (bool, optional): Export extra details for each
                collection item. Defaults to False.
            prices (bool, optional): Export the recommended prices for
                each collection item. Defaults to False.

        Returns:
            dict[str, Any]: Collection.
        """
        if self.__logger:
            self.__logger.info('Fetching Discogs collection.')
        collection = {}
        resource_path = f'/users/{self.__username}/collection/folders/0'
        releases_path = f'{resource_path}/releases'
        request = self.__requests.request
        try:
            collection_info = request(path=resource_path, params={'page': 1})
            albums = int(collection_info.get('count', 0))
            pages = -(-albums // self.DiscogsRequests.API_LIMIT) + 1
            collection = self.__get_discogs_data(
                pages=pages,
                releases_path=releases_path,
                label='Collection',
                details=details,
                prices=prices)
        except DiscogsException as de:
            if self.__logger:
                self.__logger.error('Fetching Discogs collection failled.')
                self.__logger.debug(de)
        except Exception as e:  # pylint: disable=broad-except
            if self.__logger:
                self.__logger.error('Unable to get Discogs data.')
                self.__logger.debug(e)
        return {'username': self.__username, 'collection': collection}

    def get_wantlist(
            self,
            details: Optional[bool] = False,
            prices: Optional[bool] = False) -> dict[str, Any]:
        """Fetch Discogs albums from the user's wantlist.

        Args:
            details (bool, optional): Export extra details for each
                wantlist item. Defaults to False.
            prices (bool, optional): Export the recommended prices for
                each wantlist item. Defaults to False.

        Returns:
            dict[str, Any]: Wantlist.
        """
        if self.__logger:
            self.__logger.info('Fetching Discogs wantlist.')
        wantlist = {}
        releases_path = f'/users/{self.__username}/wants'
        request = self.__requests.request
        try:
            wantlist_info = request(path=releases_path)
            pages = int(wantlist_info['pagination'].get('pages', 0)) + 1
            wantlist = self.__get_discogs_data(
                pages=pages,
                releases_path=releases_path,
                label='Wantlist',
                details=details,
                prices=prices)
        except DiscogsException as de:
            if self.__logger:
                self.__logger.error('Fetching Discogs collection failled.')
                self.__logger.debug(de)
        except Exception as e:  # pylint: disable=broad-except
            if self.__logger:
                self.__logger.error('Unable to get Discogs data.')
                self.__logger.debug(e)
        return {'username': self.__username, 'wantlist': wantlist}
