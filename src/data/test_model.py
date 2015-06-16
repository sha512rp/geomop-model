# -*- coding: utf-8 -*-
"""
Tests for model data structure.

@author: Tomas Krizek
"""

import unittest

from . import model


class TestModel(unittest.TestCase):

    def test_path_to_keys(self):
        path = '/path/to/not_this/../but_this/./1'
        expected = ('path', 'to', 'but_this', 1)
        keys = model.path_to_keys(path)
        self.assertSequenceEqual(keys, expected)

        with self.assertRaises(Exception):
            model.path_to_keys('/..')


    def test_get(self):
        root_node = {
            'problem': {
                'one': 1,
                'two': True,
                'three': [
                    {
                    'a': 2
                    },
                    {
                    'a': 3
                    }
                ]
            },
            'data': [True, False]
        }

        self.assertEqual(model.get(root_node, '/problem/one'), 1)
        self.assertEqual(model.get(root_node, '/problem/two'), True)
        self.assertEqual(model.get(root_node, '/problem/three/0/a'), 2)
        self.assertEqual(model.get(root_node, '/problem/three/1/a'), 3)
        self.assertEqual(model.get(root_node, 'data/0/../1'), False)

    def test_get_by_keys(self):
        root_node = {'problem': [True]}
        self.assertEqual(model.get_by_keys(root_node, ['problem', 0]), True)
        self.assertEqual(model.get_by_keys(root_node, ['problem', '0']), True)
