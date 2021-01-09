#!/usr/bin/env python
# coding: utf8

"""
Flask data processing
"""

import re
from unidecode import unidecode
import requests


# HTML cleaner
html_cleaner = re.compile('<.*?>')


def format_entry(entry):
    # To be removed from inputs
    d = "_" or "|" or "/" or ":" or "," or '"'
    return unidecode(entry.lower().replace(d, '').replace("'", " ").replace("&", "%26"))


def call_api(url, params):
    s = requests.Session()
    res = s.get(url=url, params=params).json()

    return res
