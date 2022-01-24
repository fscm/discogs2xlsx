#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# copyright: 2020-2022, Frederico Martins
# author: Frederico Martins <http://github.com/fscm>
# license: SPDX-License-Identifier: MIT

"""Setup discogs2xlsx."""

from setuptools import find_packages, setup
from discogs2xlsx import (
    __author__, __license__, __project__, __version__)


CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Topic :: Utilities',
    'Typing :: Typed']
DESCRIPTION = 'Exports your Discogs collection or wantlist into a xlsx file.'
ENTRY_POINTS={
    'console_scripts': [f'{__project__} = {__project__}.__main__:main']}
KEYWORDS = ['discogs', 'xlsx']
PROJECT_URLS = {
    'Documentation': f'http://fscm.github.io/{__project__}',
    'Source': f'https://github.com/fscm/{__project__}'}
PYTHON_REQUIRES = '>=3.9, <4'
URL = f'https://github.com/fscm/{__project__}'


with open('requirements.txt', 'r', encoding='utf-8') as r:
    DEPENDENCIES = [p.strip() for p in r if not p.strip().startswith('#')]

with open('README.md', 'r', encoding='utf-8') as d:
    LONG_DESCRIPTION = d.read()


if __name__ == '__main__':
    setup(
        author=__author__,
        classifiers=CLASSIFIERS,
        description=DESCRIPTION,
        entry_points=ENTRY_POINTS,
        install_requires=DEPENDENCIES,
        keywords=KEYWORDS,
        license=__license__,
        license_files=['LICENSE'],
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        name=__project__,
        package_data={__project__: ['py.typed', '*.pyi']},
        packages=find_packages(exclude=['tests']),
        project_urls=PROJECT_URLS,
        python_requires=PYTHON_REQUIRES,
        url=URL,
        version=__version__)
