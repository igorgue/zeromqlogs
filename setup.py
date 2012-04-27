# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='zeromqlogs',
    version='0.0.1',
    description='Send your Django logs via 0MQ',
    long_description=readme,
    author='Igor Guerrero',
    author_email='igfgt1@gmail.com',
    url='https://github.com/igorgue/zeromqlogs',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

