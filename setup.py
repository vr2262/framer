#!/usr/bin/env python3
from framer import __version__
from setuptools import setup, find_packages

setup(
    name='framer',
    version=__version__,
    description='desc',
    author='Viktor Roytman',
    author_email='viktor.roytman@gmail.com',
    install_requires=['pillow'],
    packages=find_packages(),
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          # haven't tested these yet:
          # 'Operating System :: MacOS :: MacOS X',
          # 'Operating System :: Windows',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
