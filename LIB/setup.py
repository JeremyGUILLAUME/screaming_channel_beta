#!/usr/bin/env python

#python2 -m pip install -e .

from setuptools import setup, find_packages

setup(
    name='sca',
    version='1.0',
    description="Side-Channel Attack Tools",
    long_description=open('README.md').read(),
    author="Jeremy GUILLAUME",
    author_email='jeremy.guillaume@centralesupelec.fr',
    license='',
    url='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'pyserial',
        'numpy',
        'matplotlib',
        'scipy'
    ],
    python_requires='~=3.8',
)
