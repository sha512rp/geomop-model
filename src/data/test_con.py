# -*- coding: utf-8 -*-
"""
Tests for con data structure

@author: Tomas Krizek
"""


import unittest
from geomopcontext.data.con import *
from geomopcontext.data.format import _FormatSpec as FormatSpec


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
        refs = ConFileHandler._extract_references(raw)

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

        root = ConFileHandler._parse_json(raw)
        with self.assertRaises(ReferenceError):
            root.get('/a').value

    def test_reference_error(self):
        raw = {
            'a': {'REF': '/b/x'},
            'b': {'REF': '/c'},
            'c': {'REF': '/a'}
        }

        with self.assertRaises(ReferenceError):
            root = ConFileHandler._parse_json(raw)
            
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
        root = ConFileHandler._parse_json(raw)

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
        root = ConFileHandler._parse_json(raw)

        self.assertEqual(root.get('/a/y')._ref, root.get('/b')._ref)


class TestDataNode(unittest.TestCase):

    def test_value(self):
        raw = 3
        data = DataNode(raw)
        self.assertEqual(data.value, 3)

    def test_record(self):
        raw = {
            'one': True,
            'two': 42
        }
        data = DataNode(raw)
        self.assertEqual(data.value['one'].value, True)
        self.assertEqual(data.value['two'].value, 42)

        with self.assertRaises(KeyError):
            data.value['three']

    def test_array(self):
        raw = [
            34,
            55,
            66,
            4
        ]
        data = DataNode(raw)
        self.assertEqual(data.value[0].value, 34)
        self.assertEqual(data.value[1].value, 55)
        self.assertEqual(data.value[2].value, 66)
        self.assertEqual(data.value[3].value, 4)

        data.value.append(DataNode(33))
        self.assertEqual(data.value[4].value, 33)

    def test_complex(self):
        raw = {
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
        data = DataNode(raw)
        self.assertEqual(data.value['problem'].value['one'].value, 1)
        self.assertEqual(data.value['problem'].value['two'].value, True)
        self.assertEqual(
            data.value['problem'].value['three'].value[0].value['a'].value, 2)
        self.assertEqual(
            data.value['problem'].value['three'].value[1].value['a'].value, 3)
        self.assertEqual(data.value['data'].value[0].value, True)
        self.assertEqual(data.value['data'].value[1].value, False)

    def test_ref(self):
        raw = {
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
            'data': [True, False],
            'problem2': None
        }
        data = DataNode(raw)
        data.value['problem2'].ref = data.value['problem']  # set reference

        self.assertEqual(data.value['problem'].value['two'].value, True)
        data.value['problem2'].value['two'].value = False  # change reference
        self.assertEqual(data.value['problem'].value['two'].value, False)
        self.assertEqual(data.value['problem2'].value['two'].value, False)

        self.assertEqual(data.value['problem2'].value['one'].value, 1)
        data.value['problem'].value['one'].value = 5  # change original
        self.assertEqual(data.value['problem2'].value['one'].value, 5)
        self.assertEqual(data.value['problem'].value['one'].value, 5)

        data.value['problem2'].value = {}
        self.assertEqual(len(data.value['problem'].value), 0)
        self.assertEqual(len(data.value['problem2'].value), 0)

    def test_get(self):
        raw = {
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
        data = DataNode(raw)
        self.assertEqual(data.get('/'), data)
        self.assertEqual(data.get('/problem/three/1/a').value, 3)  # absolute
        self.assertEqual(data.get('problem/three/1/a').value, 3)  # relative

        problem = data.get('/problem')
        self.assertEqual(problem.get('/problem'), problem)
        self.assertEqual(problem.get('/problem/one').value, 1)
        self.assertEqual(problem.get('three/0/a').value, 2)  # relative
        self.assertEqual(problem.get('../data/0').value, True)


        with self.assertRaises(LookupError):
            data.get('invalid/path')
            data.get('/invalid_key')
            data.get('/problem/invalid_key')

