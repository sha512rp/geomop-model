# -*- coding: utf-8 -*-
"""
Tests for con data structure

@author: Tomas Krizek
"""


import unittest
from geomopcontext.data.format import FormatSpec
from geomopcontext.data.con import *


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


        with self.assertRaises(LookupError):
            data.get('invalid/path')
            data.get('/invalid_key')
            data.get('/problem/invalid_key')

