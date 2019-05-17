#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2019 YugaByte, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.  See the License for the specific language governing permissions and limitations under
# the License.

from setuptools import setup, find_packages
import os

GITHUB_ORG_NAME = 'yugabyte'
PROJECT_NAME = 'ypack'

tests_require = [
    'nose',
    'tox'
]

docs_require = [
    'sphinx',
    'sphinx_rtd_theme'
]

release_require = [
    'twine',
]

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name=PROJECT_NAME,
    version='0.1.0',
    description='A way to create binary packages that can be installed in any directory',
    long_description=readme,
    author='Mikhail Bautin',
    author_email='mbautin@users.noreply.github.com',
    url='https://github.com/%s/%s' % (GITHUB_ORG_NAME, PROJECT_NAME),
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    extras_require={
        'tests': tests_require,
        'docs': docs_require,
        'release': release_require
    },
    entry_points={
        'console_scripts': [
            'ypack = ypack.ypack_tool:main'
        ]
    }
)

