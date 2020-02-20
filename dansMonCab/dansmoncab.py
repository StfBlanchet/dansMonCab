#! /usr/bin/env python3
# coding: utf-8

"""
dansMonCab chatbot
File that manages the app routes.
"""

from flask import render_template, request, jsonify
from dansMonCab import app
from dansMonCab.forms import *
from dansMonCab.scraper import *


@app.route('/')
@app.route('/home')
def home():
    # Main page providing chat interface.
    form = SearchForm(meta={'csrf': False})
    return render_template("dialog.html", title='Dans mon cab !', form=form)


@app.route('/search', methods=['POST', 'GET'])
def process_entry():
    if request.method == 'POST':
        entry = request.form['user_entry']
        driver = Driver(entry)
        driver.get_entity()

        return jsonify({
            'entity': driver.entity,
            'brief': driver.brief,
            'info': driver.info,
            'address': driver.address,
            'city': driver.city,
            'g_map': driver.g_map,
            'news': driver.news,
            'extract': driver.extract,
            'ner': driver.ner,
            'link': driver.link,
            'reply': driver.reply,
            'end_reply': driver.end_reply
        })
