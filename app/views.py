#!/usr/bin/env python
# coding: utf8

"""
Flask views
"""

from app import app
from flask import render_template, request, jsonify
from .api_bot.forms import SearchForm
from .api_bot.bot import Bot


@app.route('/')
def home():
    form = SearchForm(meta={'csrf': False})
    return render_template("dialog.html", title='Dans mon cab !', form=form)


@app.route('/search', methods=['POST'])
def search():
    entry = request.form['user_entry']
    bot = Bot(entry)
    bot.get_content()
    data = {
        'entity': bot.entity,
        'intro': bot.intro,
        'extract': bot.extract,
        'map': bot.g_map,
        'news': bot.g_news,
        'link': bot.link,
        'ok_reply': bot.ok_reply,
        'nok_reply': bot.nok_reply
    }

    return jsonify(data)
