#!/usr/bin/env python
# coding: utf8

"""
Flask init and config
"""


from flask import Flask
from os import urandom


app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(32)


from app import views
