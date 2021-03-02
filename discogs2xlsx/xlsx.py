# -*- coding: UTF-8 -*-
#
# copyright: 2020-2021, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Xlsx file creator.

This module allows for data to be writen into xlsx files.

The following is a simple usage example::
  from .xlsx import Xlsx
  x = Xlsx()
  x.save_collection({}, 'my_collection.xlsx')

The module contains the following public classes:
  - Xlsx -- The main entry point. As the example above shows, the
    Xlsx() class can be used to save data to xlsx files.

All other classes in this module are considered implementation details.
"""

from datetime import datetime
from typing import Any, Optional, TYPE_CHECKING
from progress.bar import Bar
import xlsxwriter
from . import __project__, __version__

if TYPE_CHECKING:
    from .logger import Logger

# type aliases
Workbook = xlsxwriter.workbook.Workbook
Worksheet = xlsxwriter.worksheet.Worksheet


class Xlsx:
    """Xlsx files writer.

    This class contains methods to write data into xlsx files.

    Args:
      logger (logger.Logger, optional): Logger to use. Defaults to
        None.
    """

    def __init__(self, logger: Optional['Logger'] = None) -> None:
        self.__logger = logger

    def _populate_worksheet(
            self,
            workbook: Workbook,
            worksheet: Worksheet,
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
        show_progress = True
        if self.__logger and self.__logger.level < self.__logger.Level.INFO:
            show_progress = False
        for artist in Bar('Collection').iter(
                sorted(
                    data.keys())) if show_progress else sorted(
                data.keys()):
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
                    data[artist][release]['format_qty'],
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

    def save_collection(
            self,
            collection: dict[str, Any],
            to_file: str) -> None:
        """Writes the collection information to a file.

        Args:
          collection (dict): collection to save.
          to_file (str): file to write to.
        """
        if self.__logger:
            self.__logger.info(f'Saving data to "{to_file}"')
        workbook = xlsxwriter.Workbook(to_file, {'constant_memory': True})
        workbook.set_properties({
            'title': 'Discogs Collection',
            'subject': 'User collection',
            'author': __project__,
            'created': datetime.utcnow().replace(microsecond=0),
            'comments': f'Created with {__project__} version {__version__}'})
        worksheet = workbook.add_worksheet('collection')
        self._populate_worksheet(workbook, worksheet, collection)
        workbook.close()

    def save_wantlist(self, wantlist: dict[str, Any], to_file: str) -> None:
        """Writes the wantlist information to a file.

        Args:
          wantlist (dict): wantlist to save.
          to_file (str): file to write to.
        """
        if self.__logger:
            self.__logger.info(f'Saving data to "{to_file}"')
        workbook = xlsxwriter.Workbook(to_file, {'constant_memory': True})
        workbook.set_properties({
            'title': 'Discogs Wantlist',
            'subject': 'User wantlist',
            'author': __project__,
            'created': datetime.utcnow().replace(microsecond=0),
            'comments': f'Created with {__project__} version {__version__}'})
        worksheet = workbook.add_worksheet('wantlist')
        self._populate_worksheet(workbook, worksheet, wantlist)
        workbook.close()
