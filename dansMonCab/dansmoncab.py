#! /usr/bin/env python3
# coding: utf-8

"""
dansMonCab chatbot
File that manages the app routes.
"""

from flask import render_template, request, jsonify
from dansMonCab import app
from dansMonCab.forms import *
from dansMonCab.parser import *


@app.route('/')
@app.route('/home')
def home():
    # Main page providing chat interface.
    form = SearchForm(meta={'csrf': False})
    return render_template("dialog.html", title='Dans mon cab !', form=form)


@app.route('/search', methods=['POST'])
def process_entry():
    # Launch user input processing.
    entry = request.form['user_entry']
    driver = Driver(entry)
    driver.parse()

    return jsonify({
        'status': driver.status,
        'reply': driver.reply,
        'end_reply': driver.end_reply,
        'address': driver.address,
        'g_map': driver.g_map,
        'entity': driver.entity,
        'extract': driver.extract,
        'link': driver.link
    })
