# -*- coding: UTF-8 -*-
#
# copyright: 2020-2022, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Discogs data handler.

This module handles Discogs data.

The following is a simple usage example::

    >>> from ._discogs import Discogs
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
from typing import Any, Final, Optional, TypeVar
from progress.bar import Bar
from requests.sessions import Session


__all__ = [
    'Discogs',
    'DiscogsException']


Logger = TypeVar('Logger')


class DiscogsException(Exception):
    """Generic Discogs API exception."""


class _DiscogsSession():
    """Discogs Session.

    This class will handle the requests made to the discogs API.

    Args:
        token (str): Discogs token.
        user_agent (str, optional): User agent description.
    """

    API_BASEURL: Final[str] = 'https://api.discogs.com'
    API_FORMAT: Final[str] = 'application/vnd.discogs.v2.plaintext+json'
    API_LIMIT: Final[int] = 100
    API_RATELIMIT: Final[int] = 60
    API_RATELIMIT_STATUS: Final[int] = 429
    API_RATELIMIT_TIME: Final[int] = 60
    API_UNAUTHORIZED_STATUS: Final[int] = 401

    def __init__(self, token: str, user_agent: Optional[str] = None) -> None:
        self._token = token
        self._api_last_block_time = time()
        self._headers = {
            'Accept': self.API_FORMAT,
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json'}
        self._params = {
            'token': f'{self._token}',
            'per_page': self.API_LIMIT}
        self._remaining_queries = self.API_RATELIMIT
        self._session = Session()
        if user_agent:
            self._headers['User-Agent'] = user_agent

    def get(
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
        if self._remaining_queries < 2:
            now = time()
            sleep(max(2, self.API_RATELIMIT_TIME - (
                now - self._api_last_block_time)))
            self._api_last_block_time = now
        response = self._session.get(
            f'{self.API_BASEURL}{path}',
            params={**self._params, **params} if params else self._params,
            headers=self._headers)
        headers = response.headers
        status_code = response.status_code
        self._remaining_queries = int(
            headers.get(
                'X-Discogs-Ratelimit-Remaining',
                self.API_RATELIMIT))
        if status_code == self.API_UNAUTHORIZED_STATUS:
            raise DiscogsException('Unauthorized request.')
        if status_code == self.API_RATELIMIT_STATUS:
            self._remaining_queries = 0
            return self.get(path=path, params=params)
        return loads(response.content)


class Discogs:
    """Data handler.

    This class loads data from Discogs.

    Args:
        token (str): Discogs token.
        user_agent (str, optional): User agent description.
        currency (str, optional): Currency for prices (one of 'AUD'
            'BRL' 'CAD' 'CHF' 'EUR' 'GBP' 'JPY' 'MXN' 'NZD' 'SEK' 'USD'
            'ZAR'). Defaults to 'EUR'.
        logger (logger.Logger, optional): Logger to use. Defaults to
            None.
    """

    __slots__ = (
        '_currency',
        '_identity',
        '_logger',
        '_session',
        '_username')

    def __init__(
            self,
            token: str,
            user_agent: Optional[str] = None,
            currency: Optional[str] = 'EUR',
            logger: Optional[Logger] = None) -> None:
        self._session = _DiscogsSession(token, user_agent)
        self._currency = currency
        self._logger = logger
        try:
            self._identity = self._session.get(path='/oauth/identity')
            self._username = self._identity['username']
        except DiscogsException as discogs_exception:
            if self._logger:
                self._logger.error('Invalid Discogs key.')
                self._logger.debug(discogs_exception)
            sys.exit(1)

    def _get_data(
            self,
            path: str,
            pages: int,
            label: str = 'Data',
            details: Optional[bool] = False,
            prices: Optional[bool] = False) -> dict[str, Any]:
        """Private method to help obtaining discogs data from the
        collection and/or wantlist.

        Args:
            path (str): Path of the desired data.
            pages (int): Number of pages to fetch.
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
        get = self._session.get
        try:
            for page in Bar(f'{label:10}').iter(range(1, pages)):
                content = get(path=path, params={'page': page})
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
                    r_details = get(
                        path=f'/releases/{r_id}',
                        params={'curr_abbr': self._currency})
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
                        f'{r_details.get("lowest_price", 0):,.2f}')
                        # '{:,.2f}'.format(
                        #     r_details.get('lowest_price', 0) or 0))
            if prices:
                for artist, instance_id, r_id in Bar('Prices').iter(records):
                    r_prices = get(
                        path=f'/marketplace/price_suggestions/{r_id}')
                    data[artist][instance_id].setdefault(
                        'prices',
                        {sub(r' \(.*\)', '', key).lower().replace(
                            ' ', '_'): f'{r_prices[key]["value"]:,.2f}'
                            for key in r_prices.keys()})
                            # ' ', '_'): '{:,.2f}'.format(
                            #     r_prices[key]['value'])
                            # for key in r_prices.keys()})
        except DiscogsException as discogs_exception:
            if self._logger:
                self._logger.error('Fetching Discogs collection failled.')
                self._logger.debug(discogs_exception)
        except Exception as exception:  # pylint: disable=broad-except
            if self._logger:
                self._logger.error('Unable to get Discogs data.')
                self._logger.debug(exception)
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
        if self._logger:
            self._logger.info('Fetching Discogs collection.')
        collection = {}
        resource_path = f'/users/{self._username}/collection/folders/0'
        releases_path = f'{resource_path}/releases'
        get = self._session.get
        try:
            collection_info = get(path=resource_path, params={'page': 1})
            albums = int(collection_info.get('count', 0))
            pages = -(-albums // _DiscogsSession.API_LIMIT) + 1
            collection = self._get_data(
                path=releases_path,
                pages=pages,
                label='Collection',
                details=details,
                prices=prices)
        except DiscogsException as discogs_exception:
            if self._logger:
                self._logger.error('Fetching Discogs collection failled.')
                self._logger.debug(discogs_exception)
        except Exception as exception:  # pylint: disable=broad-except
            if self._logger:
                self._logger.error('Unable to get Discogs data.')
                self._logger.debug(exception)
        return {'username': self._username, 'collection': collection}

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
        if self._logger:
            self._logger.info('Fetching Discogs wantlist.')
        wantlist = {}
        releases_path = f'/users/{self._username}/wants'
        get = self._session.get
        try:
            wantlist_info = get(path=releases_path)
            pages = int(wantlist_info['pagination'].get('pages', 0)) + 1
            wantlist = self._get_data(
                path=releases_path,
                pages=pages,
                label='Wantlist',
                details=details,
                prices=prices)
        except DiscogsException as de:
            if self._logger:
                self._logger.error('Fetching Discogs collection failled.')
                self._logger.debug(de)
        except Exception as e:  # pylint: disable=broad-except
            if self._logger:
                self._logger.error('Unable to get Discogs data.')
                self._logger.debug(e)
        return {'username': self._username, 'wantlist': wantlist}
