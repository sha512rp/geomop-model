# -*- coding: utf-8 -*-
"""
Tests for con data structure

@author: Tomas Krizek
"""


import unittest
from geomopcontext.data.format import FormatSpec
from geomopcontext.data.con import *


class TestConData(unittest.TestCase):

    def test_con_value(self):
        raw = 3
        data = ConData(raw)
        self.assertEqual(data._value, 3)

    def test_con_record(self):
        raw = {
            'one': True,
            'two': 42
        }
        data = ConData(raw)
        self.assertEqual(data.one._value, True)
        self.assertEqual(data.two._value, 42)

        with self.assertRaises(AttributeError):
            data.three

    def test_con_array(self):
        raw = [
            34,
            55,
            66,
            4
        ]
        data = ConData(raw)
        self.assertEqual(data[0]._value, 34)
        self.assertEqual(data[1]._value, 55)
        self.assertEqual(data[2]._value, 66)
        self.assertEqual(data[3]._value, 4)

        for item in data._value[2:]:
            item._value = 99
        self.assertEqual(data[2]._value, 99)
        self.assertEqual(data[3]._value, 99)

        data._value.append(ConData(33))
        self.assertEqual(data[4]._value, 33)

    # def test_ref(self):
    #     data = {
    #         'bools': [True, False],
    #         'bools2': {
    #             'REF': '/bools'
    #         }
    #     }
    #     root = ConData(data, self.format)
    #     root.bools = ConData([True, False])
    #     root.bools[0].value = False
    #     root.bools2[1].value = True
    # TODO test ref and setting _value!
    #     self.assertEqual(root.bools2._ref, root.bools)
    #     self.assertEqual(root.bools2[0].value, False)
    #     self.assertEqual(root.bools[1].value, True)
