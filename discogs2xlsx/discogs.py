# -*- coding: UTF-8 -*-
#
# copyright: 2020-2021, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Discogs data handler.

This module handles Discogs data.

The following is a simple usage example::
  from .discogs import Discogs
  d = Discogs('my_discogs_secret_token')
  c = discogs.get_collection()
  print(c)

The module contains the following public classes:
  - Discogs -- The main entry point. As the example above shows, the
    Discogs() class can be used to load data from Discogs.

All other classes in this module are considered implementation details.
"""

import json
import re
from time import time, sleep
from progress.bar import Bar
from requests import sessions
from . import __project__


class Discogs:
    """Data handler.

    This class loads data from Discogs.

    Args:
      key (str): Discogs API key.
      currency (str): Currency for prices (one of 'AUD' 'BRL' 'CAD'
        'CHF' 'EUR' 'GBP' 'JPY' 'MXN' 'NZD' 'SEK' 'USD' 'ZAR').
        Defaults to 'EUR'.
      logger (logger.Logger, optional): Logger to use. Defaults to
      None.
    """

    API_BASEURL = 'https://api.discogs.com'
    API_FORMAT = 'application/vnd.discogs.v2.plaintext+json'
    API_LIMIT = 100
    API_RATELIMIT_STATUS = 429
    API_RATELIMIT_TIME = 61

    def __init__(self, key, currency='EUR', logger=None):
        self.__api_last_block_time = time()
        self.__headers = {
            'Accept': f'{self.API_FORMAT}',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/json',
            'User-Agent': f'{__project__}'}
        self.__key = key
        self.__currency = currency
        self.__logger = logger
        self.__params = {'token': f'{self.__key}', 'per_page': self.API_LIMIT}
        self.__session = sessions.Session()
        self.__identity = self.__request(f'{self.API_BASEURL}/oauth/identity')

    def __request(self, url, params=None):
        """Private method to perform a request to the Discogs API.

        Args:
          url (str): Request URL.
          params (dict[str, Any], optional): Extra requests params.
            Defaults to None.

        Returns:
          dict[str, Any]: Discogs API data.
        """
        response = self.__session.get(
            url,
            params={
                **self.__params,
                **params} if params else self.__params,
            headers=self.__headers)
        headers = response.headers
        status_code = response.status_code
        remaining_queries = int(
            headers.get(
                'X-Discogs-Ratelimit-Remaining',
                60))
        if (remaining_queries < 2) or (
                status_code == self.API_RATELIMIT_STATUS):
            if self.__logger:
                self.__logger.debug('API rate limit reacehd.')
            now = time()
            sleep(max(
                2,
                self.API_RATELIMIT_TIME - (now - self.__api_last_block_time)))
            self.__api_last_block_time = now
            return self.__request(url=url, params=params)
        return json.loads(response.content)

    def get_collection(self, details=False, prices=False):
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
        collection_info = self.__request(
            url=f'{self.__identity["resource_url"]}/collection/folders/0',
            params={'page': 1})
        albums = int(collection_info.get('count', 0))
        pages = -(-albums // self.API_LIMIT) + 1
        show_progress = True
        if self.__logger and self.__logger.level < self.__logger.Level.INFO:
            show_progress = False
        for page in Bar('Collection').iter(
                range(1, pages)) if show_progress else range(1, pages):
            if self.__logger:
                self.__logger.debug(f'Fetching page {page}')
            content = self.__request(
                f'{self.__identity["resource_url"]}'
                '/collection/folders/0/releases',
                params={'page': page})
            releases = content['releases']
            for release in releases:
                r_id = int(release['id'])
                r_instance_id = int(release['instance_id'])
                r_artist = ' - '.join(map(
                    lambda x: re.sub(r'\(\d+\)', '', x['name']).strip(),
                    release['basic_information']['artists'])).title()
                r_url = release['basic_information']['resource_url']
                collection.setdefault(r_artist, {})
                collection[r_artist].setdefault(r_instance_id, {})
                collection[r_artist][r_instance_id].setdefault(
                    'album', release['basic_information']['title'].title())
                collection[r_artist][r_instance_id].setdefault(
                    'year', int(release['basic_information']['year']))
                collection[r_artist][r_instance_id].setdefault('id', r_id)
                collection[r_artist][r_instance_id].setdefault(
                    'format',
                    ' - '.join(map(
                        lambda x: x['name'].strip(),
                        release['basic_information']['formats'])).upper())
                collection[r_artist][r_instance_id].setdefault(
                    'format_qty',
                    ' - '.join(map(
                        lambda x: x['qty'].strip(),
                        release['basic_information']['formats'])))
                collection[r_artist][r_instance_id].setdefault(
                    'instance_id', r_instance_id)
                collection[r_artist][r_instance_id].setdefault(
                    'catno',
                    ' - '.join(map(
                        lambda x: x['catno'].strip(),
                        release['basic_information']['labels'])).upper())
                collection[r_artist][r_instance_id].setdefault(
                    'styles',
                    ', '.join(map(
                        lambda x: x.strip(),
                        release['basic_information']['styles'])).title())
                collection[r_artist][r_instance_id].setdefault(
                    'thumb', release['basic_information']['thumb'])
                collection[r_artist][r_instance_id].setdefault('url', r_url)

                if details:
                    r_details = self.__request(
                        url=f'{r_url}',
                        params={'curr_abbr': self.__currency})
                    r_details_community = r_details.get('community', {})
                    collection[r_artist][r_instance_id].setdefault(
                        'have', int(r_details_community.get('have', 0)))
                    collection[r_artist][r_instance_id].setdefault(
                        'want', int(r_details_community.get('want', 0)))
                    collection[r_artist][r_instance_id].setdefault(
                        'uri', r_details.get('uri', ''))
                    collection[r_artist][r_instance_id].setdefault(
                        'notes', r_details.get('notes', ''))
                    collection[r_artist][r_instance_id].setdefault(
                        'num_for_sale', int(r_details.get('num_for_sale', 0)))
                    collection[r_artist][r_instance_id].setdefault(
                        'lowest_price',
                        '{:,.2f}'.format(
                            r_details.get('lowest_price', 0) or 0))
                if prices:
                    r_prices = self.__request(
                        url=f'{self.API_BASEURL}'
                            f'/marketplace/price_suggestions/{r_id}')
                    collection[r_artist][r_instance_id].setdefault(
                        'prices', {
                            re.sub(
                                r' \(.*\)', '', key).lower().replace(
                                ' ', '_'): '{:,.2f}'.format(
                                r_prices[key]['value']) for key in r_prices.keys()})
                if self.__logger:
                    self.__logger.debug(
                        str(collection[r_artist][r_instance_id]))
        return collection

    def get_wantlist(self, details=False, prices=False):
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
        wantlist_info = self.__request(
            url=f'{self.__identity["resource_url"]}/wants')
        pages = int(wantlist_info['pagination'].get('pages', 0)) + 1
        show_progress = True
        if self.__logger and self.__logger.level < self.__logger.Level.INFO:
            show_progress = False
        for page in Bar('Wantlist  ').iter(
                range(1, pages)) if show_progress else range(1, pages):
            if self.__logger:
                self.__logger.debug(f'Fetching page {page}')
            content = self.__request(
                f'{self.__identity["resource_url"]}/wants',
                params={'page': page})
            releases = content['wants']
            for release in releases:
                r_id = int(release['id'])
                r_artist = ' - '.join(map(
                    lambda x: re.sub(r'\(\d+\)', '', x['name']).strip(),
                    release['basic_information']['artists'])).title()
                r_url = release['basic_information']['resource_url']
                wantlist.setdefault(r_artist, {})
                wantlist[r_artist].setdefault(r_id, {})
                wantlist[r_artist][r_id].setdefault(
                    'album', release['basic_information']['title'].title())
                wantlist[r_artist][r_id].setdefault(
                    'year', int(release['basic_information']['year']))
                wantlist[r_artist][r_id].setdefault('id', r_id)
                wantlist[r_artist][r_id].setdefault(
                    'format',
                    ' - '.join(map(
                        lambda x: x['name'].strip(),
                        release['basic_information']['formats'])).upper())
                wantlist[r_artist][r_id].setdefault(
                    'format_qty',
                    ' - '.join(map(
                        lambda x: x['qty'].strip(),
                        release['basic_information']['formats'])))
                wantlist[r_artist][r_id].setdefault(
                    'catno',
                    ' - '.join(map(
                        lambda x: x['catno'].strip(),
                        release['basic_information']['labels'])).upper())
                wantlist[r_artist][r_id].setdefault('styles', ', '.join(map(
                    lambda x: x.strip(),
                    release['basic_information']['styles'])).title())
                wantlist[r_artist][r_id].setdefault(
                    'thumb', release['basic_information']['thumb'])
                wantlist[r_artist][r_id].setdefault('url', r_url)
                if details:
                    r_details = self.__request(
                        url=f'{r_url}',
                        params={'curr_abbr': self.__currency})
                    r_details_community = r_details.get('community', {})
                    wantlist[r_artist][r_id].setdefault(
                        'have', int(r_details_community.get('have', 0)))
                    wantlist[r_artist][r_id].setdefault(
                        'want', int(r_details_community.get('want', 0)))
                    wantlist[r_artist][r_id].setdefault(
                        'uri', r_details.get('uri', ''))
                    wantlist[r_artist][r_id].setdefault(
                        'notes', r_details.get('notes', ''))
                    wantlist[r_artist][r_id].setdefault(
                        'num_for_sale', int(r_details.get('num_for_sale', 0)))
                    wantlist[r_artist][r_id].setdefault(
                        'lowest_price', '{:,.2f}'.format(
                            r_details.get(
                                'lowest_price', 0) or 0))
                if prices:
                    r_prices = self.__request(
                        url=f'{self.API_BASEURL}'
                            f'/marketplace/price_suggestions/{r_id}')
                    wantlist[r_artist][r_id].setdefault(
                        'prices', {
                            re.sub(
                                r' \(.*\)', '', key).lower().replace(
                                ' ', '_'): '{:,.2f}'.format(
                                r_prices[key]['value']) for key in r_prices.keys()})
                if self.__logger:
                    self.__logger.debug(str(wantlist[r_artist][r_id]))
        return wantlist
