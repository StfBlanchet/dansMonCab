#! /usr/bin/env python3
# coding: utf-8

"""
dansMonCab scraper 
"""


from dansMonCab.reply import *
from dansMonCab.sources import *
from dansMonCab.process import *

import random
import requests
from bs4 import BeautifulSoup as bS


class Driver:

    def __init__(self, user_input):
        self.entry = user_input
        self.input = format_entry(self.entry)
        self.query = format_query(self.input)
        self.reply = str()
        self.end_reply = random.choice(next)
        self.entity = str()
        self.suggest = str()
        self.brief = str()
        self.info = str()
        self.address = str()
        self.city = str()
        self.g_map = str()
        self.brief = str()
        self.extract = str()
        self.ner = []
        self.link = str()
        self.news = {}

    def get_entity(self):

        # Scraping pattern 1
        res = requests.get(GOO + self.query).text
        soup = bS(res, features='lxml')
        try:
            entity_1 = soup.find_all("div", class_="BNeawe deIvCb AP7Wnd", limit=1)[0].get_text()
        except IndexError:
            self.entity = ''
            self.reply = random.choice(nok)
        else:
            if entity_strict_match(self.input, entity_1) is not None:
                self.entity = entity_1
                print("entity 1 :", self.entity)
                self.refresh_query()
            else:
                # Scraping pattern 2
                res = requests.get(GOO + self.query + '+adresse').text
                soup = bS(res, features='lxml')
                try:
                    entity_2 = soup.find_all("div", class_="BNeawe deIvCb AP7Wnd", limit=3)[2].get_text()
                except IndexError:
                    self.entity = ''
                    self.reply = random.choice(nok)
                else:
                    if entity_lazy_match(self.input, entity_2) is not None:
                        self.entity = entity_2
                        print("entity 2 :", self.entity)
                    else:
                        self.reply = "Cherchez-vous {} ?".format(entity_1)

                    self.refresh_query()

    def refresh_query(self):
        base = format_entry(self.entity)
        self.query = format_query(' '.join(base.split()))
        self.get_more()

    def get_more(self):
        # Scraping pattern 1
        res = requests.get(GOO + self.query).text
        soup = bS(res, features='lxml')
        info_soup = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd", limit=8)
        info_txt = [format_goo_txt(l.get_text()) for l in info_soup]
        info = []
        for elt in info_txt:
            if elt.startswith('Adresse'):
                self.address = elt.split(': ')[1]
            if elt.startswith('Siège social'):
                self.city = elt.split(': ')[1]
                info.append(elt)
            if elt.startswith('PDG'):
                info.append(elt)
            if elt.startswith('Dirigeants'):
                info.append(elt)
            if elt.startswith('Actionnaires'):
                info.append(elt)
            if elt.startswith('Filiales'):
                info.append(elt)
            if elt.startswith('Revenus') or elt.startswith("Chiffre d'affaires"):
                info.append(elt)
            if elt.startswith('Effectif') or elt.startswith("Nombre d'employés"):
                info.append(elt)
            if elt.startswith('Fondateurs') or elt.startswith('Fondateur'):
                info.append(elt)
            if elt.startswith('Création'):
                info.append(elt)
        self.info = '<br>'.join(info)
        if len(self.address) > 0:
            self.city = self.address.split()[-1]
        else:
            self.city = self.city
        if len(self.city) > 0:
            self.get_wiki()
        else:
            # Scraping pattern 2
            res = requests.get(GOO + self.query + '+adresse').text
            soup = bS(res, features='lxml')
            loc_soup = soup.find_all("div", class_="BNeawe tAd8D AP7Wnd", limit=5)[1:5]
            loc_txt = [l.get_text() for l in loc_soup]
            loc_txt_ = [elt.split()[-1] for elt in loc_txt]
            cities = [item for item in loc_txt_ if item.istitle()]
            if len(cities) > 0:
                self.city = cities[0]
            else:
                pass
            self.get_wiki()

    def get_wiki(self):
        uri = WIKI + SEARCH + self.query
        try:
            res = requests.get(uri).json()['query']['search'][0]
        except LookupError:     # include KeyError and IndexError
            self.get_news()
        else:
            title = format_entry(res['title'])
            if entity_lazy_match(title, self.entity) is None:
                self.get_news()
            else:
                uri = WIKI + PAGE + str(res['pageid'])
                page = requests.get(uri).json()['query']['pages']
                num = [i for i in page][0]
                text = page[num]['extract'].replace('etc.', '[etc]').split('.')
                base = '.'.join(text[0:2])
                self.brief = re.sub(html_cleaner, '', base)
                self.extract = '.'.join(text[2:13]) + '...'
                self.ner = get_ner_(re.sub(html_cleaner, '', self.extract))
                self.link = page[num]['fullurl']
                self.get_news()

    def get_news(self):
        # Scrap news about the entity
        res = requests.get(G_NEWS + self.query).text
        soup = bS(res, features='lxml')
        try:
            source = soup.find_all("div", class_="kCrYT", limit=6)
            header = soup.find_all("div", class_="BNeawe vvjwJb AP7Wnd", limit=3)
            subtitle = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd", limit=6)
        except IndexError:
            self.get_map()
        else:
            urls = re.findall(urlreg, str(source), re.M | re.I)
            sources = [l for l in urls if l.startswith('http')]
            if (len(header)) > 0:
                for i in range(len(header)):
                    try:
                        self.news.update({i: {
                            'header': header[i].get_text(),
                            'source': sources[2*i],
                            'subtitle': subtitle[2*i+1].get_text()
                        }})
                    except IndexError:
                        self.news.update({i: {
                            'header': header[i].get_text(),
                            'source': sources[i],
                            'subtitle': subtitle[2*i+1].get_text()
                        }})

                self.get_map()

            else:
                self.entity = ''
                self.reply = random.choice(nok)

    def get_map(self):
        if self.city != '':
            self.g_map = G_MAP + self.query + '+' + format_entry(self.city)
        else:
            q_ = unidecode(self.entity.replace(r, "%20")).split()[0:2]
            q = format_query(' '.join(q_))
            self.g_map = G_MAP + q
