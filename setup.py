#!/usr/bin/env python
from os.path import dirname, join
from setuptools import setup
from jwhat.main import VERSION


setup(
    name='jwhat',
    version=VERSION,
    description='A tool to visualize JSON files',
    long_description=open(
        join(dirname(__file__), 'README.md')).read(),
    url='https://github.com/Askannz/jwhat',
    author='Robin Lange',
    author_email='robin.langenc@gmail.com',
    license='MIT',
    packages=['jwhat'],
    entry_points={
        'console_scripts': [
            'jwhat=jwhat.main:main',
        ],
    },
    keywords=['json', 'data', 'overview', 'tree', "visualization"],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
