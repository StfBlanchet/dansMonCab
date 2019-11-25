#! /usr/bin/env python3
# coding: utf-8

"""
dansMonCab chatbot
File that allows to test scraper.
"""


from dansMonCab.parser import *
import unittest


terms0 = ['openclassroom', 'musee du louvre', 'risk&co', 'itrust', 'bertin it']
terms1 = ['orange cyberdefense', 'renault guyancourt', 'cnim']


class TestScraper(unittest.TestCase):

    def test0_get_coord(self):
        for i in range(len(terms0)):
            search_entry = terms0[i].replace(' ', '+').replace('&', '%26')
            uri = GOO + search_entry + "+adresse"
            res = requests.get(uri).text
            soup = bS(res, features='lxml')
            soup_address = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd", limit=2)[0].get_text()
            soup_entity = soup.find_all("span", class_="BNeawe tAd8D AP7Wnd", limit=2)[0].get_text()
            self.assertIsNotNone(soup_address)
            self.assertIsNotNone(soup_entity)

    def test0_1_get_coord(self):
        search_entry = terms0[1].replace(' ', '+').replace('&', '%26')
        uri = GOO + search_entry + "+adresse"
        res = requests.get(uri).text
        soup = bS(res, features='lxml')
        soup_address = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd", limit=2)[0].get_text()
        soup_entity = soup.find_all("span", class_="BNeawe tAd8D AP7Wnd", limit=2)[0].get_text()
        self.assertEqual('Rue de Rivoli, 75001 Paris', soup_address)
        self.assertEqual('Musée du Louvre', soup_entity)

    def test0_2_get_coord(self):
        search_entry = terms0[2].replace(' ', '+').replace('&', '%26')
        uri = GOO + search_entry + "+adresse"
        res = requests.get(uri).text
        soup = bS(res, features='lxml')
        soup_address = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd", limit=2)[0].get_text()
        soup_entity = soup.find_all("span", class_="BNeawe tAd8D AP7Wnd", limit=2)[0].get_text()
        self.assertEqual('38 Rue Jacques Ibert, 92300 Levallois-Perret', soup_address)
        self.assertEqual('Risk&Co', soup_entity)

    def test1_get_coord(self):
        for i in range(len(terms1)):
            search_entry = terms1[i].replace(' ', '+').replace('&', '%26')
            uri = GOO + search_entry + "+adresse"
            res = requests.get(uri).text
            soup = bS(res, features='lxml')
            soup_2 = soup.find_all("div", class_="BNeawe tAd8D AP7Wnd", limit=1)[0].get_text()
            self.assertIsNotNone(soup_2)

    def test1_1_get_coord(self):
        search_entry = terms1[0].replace(' ', '+').replace('&', '%26')
        uri = GOO + search_entry + "+adresse"
        res = requests.get(uri).text
        soup = bS(res, features='lxml')
        soup_2 = soup.find_all("div", class_="BNeawe tAd8D AP7Wnd", limit=1)[0].get_text()
        self.assertEqual("à proximité de Orange Cyberdefense, 54 Place de l'Ellipse, Nanterre", soup_2)


if __name__ == '__main__':
    unittest.main()
