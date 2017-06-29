#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='kcheck',
    version='0.0.1a',
    description='Utility for generating and checking required kernel config symbols',
    author='Sam Jorna',
    author_email='wraeth@wraeth.id.au',

    entry_points={
        'console_scripts': [
            'kcheck = kcheck.command:main'
        ]
    },

    platforms=['Linux'],
    packages=find_packages(),
    install_requires=['configargparse'],

    package_data={
        '': ['LICENSE']
    }
)
