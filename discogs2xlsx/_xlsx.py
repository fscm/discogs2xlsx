# -*- coding: UTF-8 -*-
#
# copyright: 2020-2022, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Xlsx file creator.

This module allows for data to be writen into xlsx files.

The following is a simple usage example::

  >>> from ._xlsx import Xlsx
  >>> x = Xlsx()
  >>> x.save_collection({}, 'my_collection.xlsx')

The module contains the following public classes:
  - Xlsx -- The main entry point. As the example above shows, the
    Xlsx() class can be used to save data to xlsx files.

All other classes in this module are considered implementation details.
"""

from datetime import datetime
from typing import Any, Optional, TypeVar
from progress.bar import Bar
import xlsxwriter


__all__ = [
    'Xlsx']


Logger = TypeVar('Logger')


class Xlsx:
    """Xlsx files writer.

    This class contains methods to write data into xlsx files.

    Args:
      author (str, optional): The document author. Defaults to None.
      comments (str, optional): Document comments. Defaults to None.
      logger (_logger.Logger, optional): Logger to use. Defaults to
        None.
    """

    __slots__ = (
        '_author',
        '_comments',
        '_logger')

    def __init__(
            self,
            author: Optional[str] = None,
            comments: Optional[str] = None,
            logger: Optional[Logger] = None) -> None:
        self._author = author
        self._comments = comments
        self._logger = logger

    def _populate_worksheet(
            self,
            workbook: xlsxwriter.workbook.Workbook,
            worksheet: xlsxwriter.worksheet.Worksheet,
            data: dict[str, Any]) -> None:
        """Populates a worksheet with the info.

        Args:
          workbook (xlsxwriter.workbook.Workbook): Workbook to which
            the worksheet belongs to.
          worksheet (xlsxwriter.worksheet.Worksheet): Worksheet to
            write into.
          data (dict): data to populate the worksheet cells with.
        """

        worksheet_format_bold = workbook.add_format({'bold': True})
        # worksheet_format_currency = workbook.add_format(
        #     {'num_format': f'{self.__symbol}# ##0;-{self.__symbol}# ##0'})
        worksheet_format_default = workbook.add_format(
            {'align': 'left', 'valign': 'vcenter'})
        worksheet_format_link = workbook.add_format(
            {'font_color': 'blue', 'align': 'left', 'valign': 'vcenter'})
        worksheet_format_note = workbook.add_format(
            {'text_wrap': True, 'align': 'justify', 'valign': 'vcenter'})
        worksheet_rows = [
            'Band',
            'Year',
            'Album',
            'Cat Number',
            'Format',
            'Format Quantity',
            'Styles',
            'Have',
            'Want',
            'Notes',
            'For Sale',
            'Lowest Price',
            'Mint (M)',
            'Near Mint (NM or M-)',
            'Very Good Plus (VG+)',
            'Very Good (VG)',
            'Good Plus (G+)',
            'Good (G)']
        worksheet.set_row(0, 25)
        worksheet.write_row(0, 0, worksheet_rows, worksheet_format_bold)
        worksheet.freeze_panes(1, 0)
        worksheet_row = 1
        for artist in Bar('Writing   ').iter(sorted(data.keys())):
            for release in data[artist].keys():
                worksheet.set_row(worksheet_row, 25)
                worksheet.write_string(
                    worksheet_row,
                    0,
                    artist,
                    cell_format=worksheet_format_default)
                worksheet.write_number(
                    worksheet_row,
                    1,
                    data[artist][release]['year'],
                    cell_format=worksheet_format_default)
                worksheet.write_string(
                    worksheet_row,
                    3,
                    data[artist][release]['catno'],
                    cell_format=worksheet_format_default)
                worksheet.write_string(
                    worksheet_row,
                    4,
                    data[artist][release]['format'],
                    cell_format=worksheet_format_default)
                worksheet.write_string(
                    worksheet_row,
                    5,
                    data[artist][release]['quantity'],
                    cell_format=worksheet_format_default)
                worksheet.write_string(
                    worksheet_row,
                    6,
                    data[artist][release]['styles'],
                    cell_format=worksheet_format_default)
                if data[artist][release].get('uri', None):
                    worksheet.write_url(
                        worksheet_row,
                        2,
                        data[artist][release]['uri'],
                        string=data[artist][release]['album'],
                        cell_format=worksheet_format_link)
                    worksheet.write_number(
                        worksheet_row,
                        7,
                        data[artist][release]['have'],
                        cell_format=worksheet_format_default)
                    worksheet.write_number(
                        worksheet_row,
                        8,
                        data[artist][release]['want'],
                        cell_format=worksheet_format_default)
                    worksheet.write_string(
                        worksheet_row,
                        9,
                        data[artist][release]['notes'],
                        cell_format=worksheet_format_note)
                    worksheet.write_number(
                        worksheet_row,
                        10,
                        data[artist][release]['num_for_sale'],
                        cell_format=worksheet_format_default)
                    worksheet.write_string(
                        worksheet_row,
                        11,
                        data[artist][release]['lowest_price'],
                        cell_format=worksheet_format_default)
                    if data[artist][release].get('prices', None):
                        worksheet.write_string(
                            worksheet_row,
                            12,
                            data[artist][release]['prices']['mint'],
                            cell_format=worksheet_format_default)
                        worksheet.write_string(
                            worksheet_row,
                            13,
                            data[artist][release]['prices']['near_mint'],
                            cell_format=worksheet_format_default)
                        worksheet.write_string(
                            worksheet_row,
                            14,
                            data[artist][release]['prices']['very_good_plus'],
                            cell_format=worksheet_format_default)
                        worksheet.write_string(
                            worksheet_row,
                            15,
                            data[artist][release]['prices']['very_good'],
                            cell_format=worksheet_format_default)
                        worksheet.write_string(
                            worksheet_row,
                            16,
                            data[artist][release]['prices']['good_plus'],
                            cell_format=worksheet_format_default)
                        worksheet.write_string(
                            worksheet_row,
                            17,
                            data[artist][release]['prices']['good'],
                            cell_format=worksheet_format_default)
                else:
                    worksheet.write_string(
                        worksheet_row,
                        2,
                        data[artist][release]['album'],
                        cell_format=worksheet_format_default)
                worksheet_row += 1
        if self._logger:
            self._logger.info('Data saved.')

    def save_collection(
            self,
            collection: dict[str, Any],
            to_file: str) -> None:
        """Writes the collection information to a file.

        Args:
          collection (dict): collection to save.
          to_file (str): file to write to.
        """
        if self._logger:
            self._logger.info(f'Saving data to "{to_file}".')
        workbook = xlsxwriter.Workbook(to_file, {'constant_memory': True})
        workbook.set_properties({
            'title': 'Discogs Collection',
            'subject': f'{collection.get("username", "")} collection',
            'author': self._author,
            'created': datetime.utcnow().replace(microsecond=0),
            'comments': self._comments})
        worksheet = workbook.add_worksheet('collection')
        self._populate_worksheet(
            workbook,
            worksheet,
            collection.get('collection',{} ))
        workbook.close()

    def save_wantlist(self, wantlist: dict[str, Any], to_file: str) -> None:
        """Writes the wantlist information to a file.

        Args:
          wantlist (dict): wantlist to save.
          to_file (str): file to write to.
        """
        if self._logger:
            self._logger.info(f'Saving data to "{to_file}".')
        workbook = xlsxwriter.Workbook(to_file, {'constant_memory': True})
        workbook.set_properties({
            'title': 'Discogs Wantlist',
            'subject': f'{wantlist.get("username", "")} wantlist',
            'author': self._author,
            'created': datetime.utcnow().replace(microsecond=0),
            'comments': self._comments})
        worksheet = workbook.add_worksheet('wantlist')
        self._populate_worksheet(
            workbook,
            worksheet,
            wantlist.get('wantlist', {}))
        workbook.close()
