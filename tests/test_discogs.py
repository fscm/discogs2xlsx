# -*- coding: UTF-8 -*-
#
# copyright: 2020-2021, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Tests for the Discogs module."""

# import sys
# import pytest
from discogs2xlsx.discogs import Discogs
from discogs2xlsx.logger import Logger


def test_discogs_ok_default(mocker):
    """test_discogs_ok_default

    Test if Discogs can be instantiated.

    Args:
      mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    response = {
        'id': 1234567,
        'username': 'dummy',
        'resource_url': 'https://api.discogs.com/users/dummy',
        'consumer_name': 'dummy'}
    # mocker.patch(
    #     'discogs2xlsx.discogs.Discogs._Discogs__request',
    #     return_value=response)
    mocker.patch(
        'discogs2xlsx.discogs.Discogs.DiscogsRequests.request',
        return_value=response)
    d = Discogs(key='dummy')
    assert isinstance(d, Discogs)
    assert d._Discogs__identity == response  # pylint: disable=protected-access)


def test_discogs_ok_collection(mocker):
    """test_discogs_ok_default

    Test if Discogs can obtain a collection.

    Args:
      mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    response_0 = {
        'id': 1234567,
        'username': 'dummy',
        'resource_url': 'https://api.discogs.com/users/dummy',
        'consumer_name': 'dummy'}
    response_1 = {
        'id': 0,
        'name': 'All',
        'count': 1,
        'resource_url':
            'https://api.discogs.com/users/dummy/collection/folders/0'}
    response_2 = {
        'pagination': {
            'page': 1,
            'pages': 1,
            'per_page': 100,
            'items': 1,
            'urls': {}},
        'releases': [{
            'id': 12736525,
            'instance_id': 382774613,
            'date_added': '2019-06-18T20:35:01-07:00',
            'rating': 3,
            'basic_information': {
                'id': 12736525,
                'master_id': 1446356,
                'master_url': 'https://api.discogs.com/masters/1446356',
                'resource_url': 'https://api.discogs.com/releases/12736525',
                'thumb': 'https://img.discogs.com/dummy.jpg',
                'cover_image': 'https://img.discogs.com/dummy.jpg',
                'title': 'Dionysus',
                'year': 2018,
                'formats': [{
                    'name': 'Vinyl',
                    'qty': '1',
                    'descriptions': ['LP', 'Album']}],
                'labels': [{
                    'name': '[pias]',
                    'catno': 'PIASR440LP',
                    'entity_type': '1',
                    'entity_type_name': 'Label',
                    'id': 133449,
                    'resource_url': 'https://api.discogs.com/labels/133449'}],
                'artists': [{
                    'name': 'Dead Can Dance',
                    'anv': '',
                    'join': '',
                    'role': '',
                    'tracks': '',
                    'id': 12368,
                    'resource_url': 'https://api.discogs.com/artists/12368'}],
                'genres': ['Folk, World, & Country'],
                'styles': [
                    'Modern Classical',
                    'Downtempo',
                    'New Age']},
            'folder_id': 2327149}]}
    response_3 = {
        'id': 12736525,
        'status': 'Accepted',
        'year': 2018,
        'resource_url': 'https://api.discogs.com/releases/12736525',
        'uri': 'https://www.discogs.com/Dead-Can-Dance-Dionysus/release/12736525',
        'artists': [],
        'artists_sort': 'Dead Can Dance',
        'labels': [],
        'series': [],
        'companies': [],
        'formats': [],
        'data_quality': 'Needs Vote',
        'community': {
            'have': 2533,
            'want': 323,
            'rating': {'count': 294, 'average': 4.37},
            'submitter': {
                'username': 'dummy',
                'resource_url': 'https://api.discogs.com/users/dummy'},
            'contributors': [],
            'data_quality': 'Needs Vote',
            'status': 'Accepted'},
        'format_quantity': 1,
        'date_added': '2018-10-31T04:27:07-07:00',
        'date_changed': '2019-02-01T10:27:51-08:00',
        'num_for_sale': 153,
        'lowest_price': 14.46,
        'master_id': 1446356,
        'master_url': 'https://api.discogs.com/masters/1446356',
        'title': 'Dionysus',
        'country': 'Europe',
        'released': '2018-11-02',
        'notes': '\u2117 2018 Dead Can Dance\n\u00a9 2018 Dead Can Dance.',
        'released_formatted': '02 Nov 2018',
        'identifiers': [],
        'videos': [],
        'genres': ['Folk, World, & Country'],
        'styles': ['Modern Classical', 'Downtempo', 'New Age'],
        'tracklist': [],
        'extraartists': [],
        'images': [],
        'thumb': '',
        'estimated_weight': 230}
    response_4 = {
        'Mint (M)': {'currency': 'EUR', 'value': 24.43},
        'Near Mint (NM or M-)': {'currency': 'EUR', 'value': 21.86},
        'Very Good Plus (VG+)': {'currency': 'EUR', 'value': 16.71},
        'Very Good (VG)': {'currency': 'EUR', 'value': 11.57},
        'Good Plus (G+)': {'currency': 'EUR', 'value': 6.43},
        'Good (G)': {'currency': 'EUR', 'value': 3.86},
        'Fair (F)': {'currency': 'EUR', 'value': 2.58},
        'Poor (P)': {'currency': 'EUR', 'value': 1.29}}
    result = {
        'username': 'dummy',
        'collection': {
            'Dead Can Dance': {
                382774613: {
                    'album': 'Dionysus',
                    'year': 2018,
                    'id': 12736525,
                    'format': 'VINYL',
                    'quantity': '1',
                    'instance_id': 382774613,
                    'catno': 'PIASR440LP',
                    'styles': 'Modern Classical, Downtempo, New Age',
                    'url': 'https://api.discogs.com/releases/12736525',
                    'have': 2533,
                    'want': 323,
                    'uri': 'https://www.discogs.com/Dead-Can-Dance-Dionysus/release/12736525',
                    'notes': '℗ 2018 Dead Can Dance\n© 2018 Dead Can Dance.',
                    'num_for_sale': 153,
                    'lowest_price': '14.46',
                    'prices': {
                        'mint': '24.43',
                        'near_mint': '21.86',
                        'very_good_plus': '16.71',
                        'very_good': '11.57',
                        'good_plus': '6.43',
                        'good': '3.86',
                        'fair': '2.58',
                        'poor': '1.29'}}}}}
    # mocker.patch(
    #     'discogs2xlsx.discogs.Discogs._Discogs__request',
    #     side_effect=[
    #         response_0, response_1, response_2, response_3, response_4])
    mocker.patch(
        'discogs2xlsx.discogs.Discogs.DiscogsRequests.request',
        side_effect=[
            response_0, response_1, response_2, response_3, response_4])
    l = Logger(level=Logger.Level.NONE)
    d = Discogs(key='dummy', logger=l)
    c = d.get_collection(details=True, prices=True)
    assert isinstance(d, Discogs)
    assert c == result


def test_discogs_ok_wantlist(mocker):
    """test_discogs_ok_default

    Test if Discogs can obtain a wantlist.

    Args:
      mocker (pytest_mock.plugin.MockerFixture): Mocker.
    """
    response_0 = {
        'id': 1234567,
        'username': 'dummy',
        'resource_url': 'https://api.discogs.com/users/dummy',
        'consumer_name': 'dummy'}

    response_1 = {
        'pagination': {
            'page': 1,
            'pages': 1,
            'per_page': 100,
            'items': 1,
            'urls': {}},
        'wants': [{
            'id': 3099920,
            'resource_url': 'https://api.discogs.com/users/dummy/wants/3099920',
            'rating': 0,
            'date_added': '2018-09-25T02:12:31-07:00',
            'basic_information': {
                'id': 3099920,
                'master_id': 42496,
                'master_url': 'https://api.discogs.com/masters/42496',
                'resource_url': 'https://api.discogs.com/releases/3099920',
                'title': 'Lunar Womb',
                'year': 2006,
                'formats': [{
                    'name': 'Vinyl',
                    'qty': '1',
                    'text': 'Red',
                    'descriptions': [
                        'LP',
                        'Album',
                        'Limited Edition',
                        'Reissue',
                        'Remastered']}],
                'labels': [{
                    'name': '20 Buck Spin',
                    'catno': 'spin:004',
                    'entity_type': '1',
                    'entity_type_name': 'Label',
                    'id': 42593,
                    'resource_url': 'https://api.discogs.com/labels/42593'}],
                'artists': [{
                    'name': 'The Obsessed',
                    'anv': '',
                    'join': '',
                    'role': '',
                    'tracks': '',
                    'id': 311946,
                    'resource_url': 'https://api.discogs.com/artists/311946'}],
                'thumb': 'https://img.discogs.com/dummy.jpg',
                'cover_image': 'https://img.discogs.com/dummy.jpg',
                'genres': ['Rock'],
                'styles': ['Stoner Rock', 'Doom Metal', 'Heavy Metal']},
            'notes': ''}]}
    response_2 = {
        'id': 3099920,
        'status': 'Accepted',
        'year': 2006,
        'resource_url': 'https://api.discogs.com/releases/3099920',
        'uri': 'https://www.discogs.com/The-Obsessed-Lunar-Womb/release/3099920',
        'artists': [],
        'artists_sort': 'Obsessed, The',
        'labels': [],
        'series': [],
        'companies': [],
        'formats': [],
        'data_quality': 'Needs Vote',
        'community': {
            'have': 73,
            'want': 120,
            'rating': {'count': 13, 'average': 4.46},
            'submitter': {
                'username': 'dummy',
                'resource_url': 'https://api.discogs.com/users/dummy'},
            'contributors': [],
            'data_quality': 'Needs Vote',
            'status': 'Accepted'},
        'format_quantity': 1,
        'date_added': '2011-09-11T03:51:00-07:00',
        'date_changed': '2014-12-05T09:07:02-08:00',
        'num_for_sale': 1,
        'lowest_price': 60,
        'master_id': 42496,
        'master_url': 'https://api.discogs.com/masters/42496',
        'title': 'Lunar Womb',
        'country': 'US',
        'released': '2006',
        'notes': 'Pressing Info:\r\n\r\n1000 Black\r\n300 Red\r\n',
        'released_formatted': '2006',
        'identifiers': [],
        'videos': [],
        'genres': ['Rock'],
        'styles': ['Stoner Rock', 'Doom Metal', 'Heavy Metal'],
        'tracklist': [],
        'extraartists': [],
        'images': [],
        'thumb': '',
        'estimated_weight': 230}
    response_3 = {
        'Mint (M)': {'currency': 'EUR', 'value': 27.31},
        'Near Mint (NM or M-)': {'currency': 'EUR', 'value': 24.44},
        'Very Good Plus (VG+)': {'currency': 'EUR', 'value': 18.69},
        'Very Good (VG)': {'currency': 'EUR', 'value': 12.94},
        'Good Plus (G+)': {'currency': 'EUR', 'value': 7.19},
        'Good (G)': {'currency': 'EUR', 'value': 4.31},
        'Fair (F)': {'currency': 'EUR', 'value': 2.87},
        'Poor (P)': {'currency': 'EUR', 'value': 1.44}}
    result = {
        'username': 'dummy',
        'wantlist': {
            'The Obsessed': {
                3099920: {
                    'album': 'Lunar Womb',
                    'year': 2006,
                    'id': 3099920,
                    'instance_id': 3099920,
                    'format': 'VINYL',
                    'quantity': '1',
                    'catno': 'SPIN:004',
                    'styles': 'Stoner Rock, Doom Metal, Heavy Metal',
                    'url': 'https://api.discogs.com/releases/3099920',
                    'have': 73,
                    'want': 120,
                    'uri': 'https://www.discogs.com/The-Obsessed-Lunar-Womb/release/3099920',
                    'notes': 'Pressing Info:\r\n\r\n1000 Black\r\n300 Red\r\n',
                    'num_for_sale': 1,
                    'lowest_price': '60.00',
                    'prices': {
                        'mint': '27.31',
                        'near_mint': '24.44',
                        'very_good_plus': '18.69',
                        'very_good': '12.94',
                        'good_plus': '7.19',
                        'good': '4.31',
                        'fair': '2.87',
                        'poor': '1.44'}}}}}
    # mocker.patch(
    #     'discogs2xlsx.discogs.Discogs._Discogs__request',
    #     side_effect=[
    #         response_0, response_1, response_1, response_2, response_3])
    mocker.patch(
        'discogs2xlsx.discogs.Discogs.DiscogsRequests.request',
        side_effect=[
            response_0, response_1, response_1, response_2, response_3])
    l = Logger(level=Logger.Level.NONE)
    d = Discogs(key='dummy', logger=l)
    w = d.get_wantlist(details=True, prices=True)
    assert isinstance(d, Discogs)
    assert w == result
