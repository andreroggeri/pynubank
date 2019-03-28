# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='pynubank',
    version='0.17',
    url='https://github.com/andreroggeri/pynubank',
    author='André Roggeri Campos',
    author_email='a.roggeri.c@gmail.com',
    license='BSD',
    packages=['pynubank'],
    package_data={'pynubank': ['queries/*.gql']},
    install_requires=['requests', 'qrcode'],
)
