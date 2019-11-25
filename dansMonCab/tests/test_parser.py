#! /usr/bin/env python3
# coding: utf-8

"""
dansMonCab chatbot
File that allows to test NER.
"""

from dansMonCab.parser import *
import unittest


d0 = Driver("Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassroom ?")
d1 = Driver("Salut GrandPy ! Sais-tu où se trouve le musée du Louvre ?")
d2 = Driver("Bonjour, pouvez-vous me conduire chez Orange Cyberdéfense ?")
d3 = Driver("Bonjour, je souhaiterais aller chez Risk&Co.")
d4 = Driver("Emmenez-moi au musée d'Orsay, svp.")
d5 = Driver("Je suis attendue chez Bertin IT.")
d6 = Driver("J'ai rendez-vous chez Itrust.")
d7 = Driver("Je cherche l'adresse de PSA Poissy.")


class TestParser(unittest.TestCase):

    def test0_parse(self):
        elt = d0.parse()
        self.assertEqual(elt, 'openclassroom')

    def test1_parse(self):
        elt = d1.parse()
        self.assertEqual(elt, 'musee du louvre')

    def test2_parse(self):
        elt = d2.parse()
        self.assertEqual(elt, 'orange cyberdefense')

    def test3_parse(self):
        elt = d3.parse()
        self.assertEqual(elt, 'risk&co')

    def test4_parse(self):
        elt = d4.parse()
        self.assertEqual(elt, 'musee d\'orsay')

    def test5_parse(self):
        elt = d5.parse()
        self.assertEqual(elt, 'bertin it')

    def test6_parse(self):
        elt = d6.parse()
        self.assertEqual(elt, 'itrust')

    def test7_parse(self):
        elt = d7.parse()
        self.assertEqual(elt, 'psa poissy')


if __name__ == '__main__':
    unittest.main()
