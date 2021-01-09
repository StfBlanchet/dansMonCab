#!/usr/bin/env python
# coding: utf8

"""
Flask config
"""

from os import path, environ
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

NEWS_KEY = environ.get('NEWS_KEY')
SOURCE1 = environ.get('SOURCE1')
SOURCE2 = environ.get('SOURCE2')
SOURCE3 = environ.get('SOURCE3')
