#!/usr/bin/env python3
from pathlib import Path

import pkg_resources
from setuptools import setup, find_packages

with Path('README.md').open('r') as fh:
    long_description = fh.read()

with Path('requirements.txt').open('r') as fh:
    install_requires = [str(req) for req in pkg_resources.parse_requirements(fh)]

with Path('requirements-dev.txt').open('r') as fh:
    test_requires = [str(req) for req in pkg_resources.parse_requirements(fh)]

setup(
    name='{{ cookiecutter.project_name }}',
    packages=find_packages(),
    test_suite='tests',
    platforms='any',
    install_requires=install_requires,
    test_requires=test_requires,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
