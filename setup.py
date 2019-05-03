#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='relocate',
    version='0.1.0',
    description='Relocate binary packages to a new directory',
    long_description=readme,
    author='Mikhail Bautin',
    author_email='mbautin@users.noreply.github.com',
    url='https://github.com/yugabyte/relocate',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

