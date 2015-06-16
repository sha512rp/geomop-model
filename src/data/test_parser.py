# -*- coding: utf-8 -*-
"""
Tests for parser module.

@author: Tomas Krizek
"""

import unittest

from . import parser
from . import model


class TestConFileHandler(unittest.TestCase):
    def test_references(self):
        data = {
            'a': {'x': 0, 'y': {'REF': '/b/y'}},
            'b': {'REF': '/d'},
            'c': [
                {'REF': '/b/x'},
                {'REF': '/a/y'}
            ],
            'd': {'x': 3, 'y': 5}
        }

        refs = parser._extract_references(data)

        self.assertEqual(refs['/a/y'], '/b/y')
        self.assertEqual(refs['/b'], '/d')
        self.assertEqual(refs['/c/0'], '/b/x')
        self.assertEqual(refs['/c/1'], '/a/y')

    def test_reference_error(self):
        data = {
            'a': {'REF': '/b/x'},
            'b': {'REF': '/c'},
            'c': {'REF': '/a'}
        }

        with self.assertRaises(Exception):
            parser._resolve_references(data)

    def test_parse_json(self):
        data = {
            'a': {'x': 0, 'y': {'REF': '/b/y'}},
            'b': {'REF': '/d'},
            'c': [
                {'REF': '/b/x'},
                {'REF': '/a/y'}
            ],
            'd': {'x': 3, 'y': 5},
            'e': {'REF': '/c'}
        }
        parser._resolve_references(data)

        self.assertEqual(model.get(data, '/a/x'), 0)
        self.assertEqual(model.get(data, '/a/y'), 5)
        self.assertEqual(model.get(data, '/b/x'), 3)
        self.assertEqual(model.get(data, '/b/y'), 5)
        self.assertEqual(model.get(data, '/c/0'), 3)
        self.assertEqual(model.get(data, '/c/1'), 5)
        self.assertEqual(model.get(data, '/d/x'), 3)
        self.assertEqual(model.get(data, '/d/y'), 5)
        self.assertEqual(model.get(data, '/e/0'), 3)
        self.assertEqual(model.get(data, '/e/1'), 5)

        # test references
        self.assertIs(model.get(data, '/a/y'), model.get(data, '/d/y'))
        self.assertIs(model.get(data, '/b'), model.get(data, '/d'))
        self.assertIs(model.get(data, '/c/0'), model.get(data, '/d/x'))
        self.assertIs(model.get(data, '/c/1'), model.get(data, '/d/y'))
        self.assertIs(model.get(data, '/e'), model.get(data, '/c'))

    def test_relative_reference(self):
        data = {
            'a': {'x': 0, 'y': {'REF': '../../b'}},
            'b': 2,
        }
        parser._resolve_references(data)

        self.assertIs(model.get(data, '/a/y'), model.get(data, '/b'))

