# -*- coding: utf-8 -*-
"""
Tests for parser module.

@author: Tomas Krizek
"""

import unittest
from . import parser


class TestConFileHandler(unittest.TestCase):
    def test_references(self):
        raw = {
            'a': {'x': 0, 'y': {'REF': '/b/y'}},
            'b': {'REF': '/d'},
            'c': [
                {'REF': '/b/x'},
                {'REF': '/a/y'}
            ],
            'd': {'x': 3, 'y': 5}
        }
        refs = parser._extract_references(raw)

        self.assertEqual(refs['/a/y'], '/b/y')
        self.assertEqual(refs['/b'], '/d')
        self.assertEqual(refs['/c/0'], '/b/x')
        self.assertEqual(refs['/c/1'], '/a/y')

    def test_circular_reference(self):
        raw = {
            'a': {'REF': '/b'},
            'b': {'REF': '/c'},
            'c': {'REF': '/a'}
        }

        root = parser._resolve_references(raw)
        with self.assertRaises(parser.RefError):
            root.get('/a').value

    def test_reference_error(self):
        raw = {
            'a': {'REF': '/b/x'},
            'b': {'REF': '/c'},
            'c': {'REF': '/a'}
        }

        with self.assertRaises(parser.RefError):
            parser._resolve_references(raw)

    def test_parse_json(self):
        raw = {
            'a': {'x': 0, 'y': {'REF': '/b/y'}},
            'b': {'REF': '/d'},
            'c': [
                {'REF': '/b/x'},
                {'REF': '/a/y'}
            ],
            'd': {'x': 3, 'y': 5},
            'e': {'REF': '/c'}
        }
        root = parser._resolve_references(raw)

        self.assertEqual(root.get('/a/x').value, 0)
        self.assertEqual(root.get('/a/y').value, 5)
        self.assertEqual(root.get('/b/x').value, 3)
        self.assertEqual(root.get('/b/y').value, 5)
        self.assertEqual(root.get('/c/0').value, 3)
        self.assertEqual(root.get('/c/1').value, 5)
        self.assertEqual(root.get('/d/x').value, 3)
        self.assertEqual(root.get('/d/y').value, 5)
        self.assertEqual(root.get('/e/0').value, 3)
        self.assertEqual(root.get('/e/1').value, 5)

        # test references
        self.assertEqual(root.get('/a/y').value, root.get('/d/y').value)
        self.assertEqual(root.get('/b').value, root.get('/d').value)
        self.assertEqual(root.get('/c/0').value, root.get('/d/x').value)
        self.assertEqual(root.get('/c/1').value, root.get('/d/y').value)
        self.assertEqual(root.get('/e').value, root.get('/c').value)

    def test_relative_reference(self):
        raw = {
            'a': {'x': 0, 'y': {'REF': '../../b'}},
            'b': 2,
        }
        root = parser._resolve_references(raw)

        self.assertEqual(root.get('/a/y')._ref, root.get('/b')._ref)

