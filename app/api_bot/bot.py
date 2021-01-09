#!/usr/bin/env python
# coding: utf8

"""
Flask bot
"""

from .reply import *
from .utils import *
import random
from app.config import NEWS_KEY, SOURCE1, SOURCE2, SOURCE3


class Bot:

    def __init__(self, user_input):
        self.input = format_entry(user_input)
        # Define bot reply
        self.ok_reply = random.choice(next)
        self.nok_reply = random.choice(nok)
        # Define data to be displayed
        self.entity = str()
        self.link = str()
        self.intro = str()
        self.extract = str()
        self.g_news = {}
        self.g_map = str()

    def get_content(self):
        params = {'action': 'opensearch',
                  'redirects': 'resolve',
                  'search': self.input,
                  'format': 'json'}
        data = call_api(SOURCE1, params)
        # if API returns propositions
        # relative to the user input
        if data[1]:
            # Pick the first proposed entity
            self.entity = data[1][0]
            self.link = data[3][0]
            # Get the whole content relative
            # to the targeted entity
            params = {'action': 'query',
                      'format': 'json',
                      'prop': 'extracts',
                      'titles': self.entity}
            content = call_api(SOURCE1, params)
            page = content['query']['pages']
            num = [i for i in page][0]
            text = page[num]['extract'].replace('etc.', '[etc]').split('.')
            self.intro = re.sub(html_cleaner, '', '.'.join(text[0:2]))
            self.extract = re.sub(html_cleaner, '', '.'.join(text[2:8])) + '...'

            # Get google map
            self.g_map = SOURCE3 + self.entity.replace(" ", "+")

            # Get latest news
            params = {'q': self.entity,
                      'language': 'fr',
                      'sortBy': 'publishedAt',
                      'apiKey': NEWS_KEY}
            news = call_api(SOURCE2, params)
            if news['status'] == 'ok':
                self.g_news.update({'total': int(news['totalResults']), 'news': {}})
                for i, art in list(enumerate(news['articles'])):
                    self.g_news['news'].update({i: {
                        'header': art['title'],
                        'subtitle': art['content'].split('[')[0].replace('[', '...'),
                        'source': art['url'],
                        'img': art['urlToImage'],
                        'date': art['publishedAt']}
                    })
