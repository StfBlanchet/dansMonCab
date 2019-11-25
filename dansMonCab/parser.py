#! /usr/bin/env python3
# coding: utf-8

"""
dansMonCab chatbot
"""


from dansMonCab.reply import *
from dansMonCab.sources import *

import random
from bs4 import BeautifulSoup as bS
import requests
import re
from unidecode import unidecode

import spacy
nlp = spacy.load('fr_core_news_sm')


"""
This class allows to process user input
and to provide her with the information she asks for.
"""


class Driver:

    def __init__(self, user_input):
        self.input = user_input
        self.reply = str()
        self.end_reply = random.choice(next)
        self.status = str()
        self.ner = str()
        self.entity = str()
        self.address = str()
        self.search = str()
        self.g_map = str()
        self.page_id = int()
        self.extract = str()
        self.link = str()

    def parse(self):
        """
        Method to extract named entities
        from the user's input.
        """
        parser = {}
        doc = nlp(self.input.lower())
        if len(doc.ents) == 0:
            self.reply = random.choice(nok)
            self.status = 'nok'
        else:
            for ent in doc.ents:
                parser.update({'entity': ent.text, 'type': ent.label_})
            self.ner = unidecode(parser['entity'])
            self.get_coord()
            return self.ner

    def get_coord(self):
        """
        Method to get proper entity
        name and address from Google results.
        """
        terms = self.ner.replace(' ', '+').replace('&', '%26')
        uri = GOO + terms + "+adresse"
        res = requests.get(uri).text
        soup = bS(res, features='lxml')
        # pattern 1 i.e. entry is correct and has 1 address
        soup_1_entity = soup.find_all("span", class_="BNeawe tAd8D AP7Wnd", limit=2)
        soup_1_address = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd", limit=2)
        if not soup_1_address:
            # try pattern 1b i.e. inverted tags
            soup_2_entity = soup.find_all("div", class_="BNeawe deIvCb AP7Wnd", limit=1)
            soup_2_address = soup.find_all("span", class_="BNeawe tAd8D AP7Wnd", limit=1)
            if not soup_2_address:
                # try pattern 2 i.e. multiple addresses available
                soup_3_bloc = soup.find_all("div", class_="BNeawe tAd8D AP7Wnd", limit=1)
                if not soup_3_bloc:
                    # no soup 3: stop there
                    self.reply = random.choice(nok)
                    self.status = 'nok'
                else:
                    data = soup_3_bloc[0].get_text().split(',')
                    if self.ner not in unidecode(data[0].lower()):
                        # soup 2 is wrong: ask Wiki
                        self.entity = self.ner
                        self.reply = random.choice(fuzzy_map)
                    else:
                        # soup 3 succeeds:
                        self.entity = data[0].replace('à proximité de ', '')
                        self.address = data[1] + ',' + data[2]
                        self.reply = random.choice(doubt) + " {} se trouve {}.".format(
                            self.entity, data[1] + " à" + data[2])
            else:
                # soup 2 succeeds:
                self.address = soup_2_address[0].get_text()
                self.entity = soup_2_entity[0].get_text()
                self.reply = random.choice(ok) + " {} se trouve {}.".format(self.entity, self.address)
        else:
            # soup 1 succeeds:
            self.address = soup_1_address[0].get_text()
            self.entity = soup_1_entity[0].get_text()
            self.reply = random.choice(ok) + " {} se trouve {}.".format(self.entity, self.address)
        self.clean_terms()

    def clean_terms(self):
        """
        Method to properly format search terms
        for both Google maps and Wikipedia API.
        """
        self.search = self.entity.replace(' ', '%20').replace("'", '%20').replace('&', '%26')
        cleaner = '|' or '/' or ','
        self.search = self.search.split(cleaner)[0]
        self.get_map()

    def get_map(self):
        """
        Method to generate Google maps URI.
        """
        if self.search:
            self.g_map = G_MAP + self.search
            self.get_page_id()
        else:
            self.status = 'nok'
            self.reply = random.choice(nok)

    def get_page_id(self):
        """
        Method to get the page id
        of the targeted entity.
        """
        uri = WIKI + SEARCH + self.search
        r = requests.get(uri).json()
        if not r['query']['search']:
            # no wiki item neither: stop there
            self.status = 'nok'
            self.reply = random.choice(nok)
        else:
            self.page_id = r['query']['search'][0]['pageid']
            self.get_extract()

    def get_extract(self):
        """
        Method to get the summary
        of to the targeted entity.
        """
        self.status = 'ok'
        uri = WIKI + PAGE + str(self.page_id)
        r = requests.get(uri).json()
        page = r['query']['pages']
        num = [i for i in page][0]
        # remove html from the extract
        cleaner = re.compile('<.*?>')
        text = re.sub(cleaner, '', page[num]['extract']).split()
        self.extract = ' '.join(text[0:80]) + '...'
        self.link = page[num]['fullurl']
