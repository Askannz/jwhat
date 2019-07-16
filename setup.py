#!/usr/bin/env python
from os.path import dirname, join
from setuptools import setup


setup(
    name='jwhat',
    version='0.1',
    description='A tool to summarize JSON files',
    long_description=open(
        join(dirname(__file__), 'README.md')).read(),
    author='Robin Lange',
    author_email='robin.langenc@gmail.com',
    license='MIT',
    packages=['jwhat'],
    entry_points={
        'console_scripts': [
            'jwhat=jwhat.main:main',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
