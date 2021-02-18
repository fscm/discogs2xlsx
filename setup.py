#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# copyright: 2020-2021, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Setup discogs2xlsx."""

import os
from setuptools import setup
from discogs2xlsx import (
    __author__, __author_email__, __license__, __project__, __version__)

if __name__ == '__main__':
    setup(
        author=__author__,
        author_email=__author_email__,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.6',
            'Topic :: Utilities',
            'Typing :: Typed'],
        description=(
            'Exports your Discogs collection or wantlist into a xlsx file'),
        install_requires=[
            'progress>=1.5',
            'requests>=2.25.1',
            'xlsxwriter>=1.3.7'],
        license=__license__,
        long_description=open('README.md', 'r', encoding='utf-8').read(),
        long_description_content_type='text/markdown',
        name=__project__,
        packages=[__project__],
        package_data={'': ['LICENSE'], __project__: ['py.typed', '*.pyi']},
        python_requires='~=3.6',
        url='https://github.com/fscm/discogs2xlsx',
        version=__version__,
        scripts=['bin/' + __project__ + '.bat' if os.name == 'nt' else 'bin/' + __project__])
