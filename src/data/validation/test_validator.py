# -*- coding: utf-8 -*-
"""
Tests for validator

@author: Tomas Krizek
"""

import unittest
from unittest.mock import Mock

from .validator import *
from .errors import *
from ..format import _FormatSpec as FormatSpec
from ..model import DataNode


class TestValidator(unittest.TestCase):

    its_int = Mock(
        input_type='Integer',
        min=0,
        max=3)

    its_string = Mock(
        input_type='String')

    its_array = Mock(
        input_type='Array',
        subtype=its_int,
        min=1,
        max=4)

    its_record = Mock(
        spec=['input_type', 'keys', 'type_name'],
        input_type='Record',
        keys={
            'a1': {'default': {'type': 'obligatory'}, 'type': its_int},
            'a2': {'default': {'type': 'obligatory'}, 'type': its_int},
            'b': {'default': {'type': 'value at declaration'},
                'type': its_int},
            'c': {'default': {'type': 'value at read time'},
                'type': its_int},
            'd': {'default': {'type': 'optional'}, 'type': its_int},
            'TYPE': {'type': its_string}},
        type_name='MyRecord')

    its_record2 = Mock(
        spec=['input_type', 'keys', 'type_name'],
        input_type='Record',
        keys={
            'b': {'default': {'type': 'obligatory'}, 'type': its_int},
            'TYPE': {'type': its_string}},
        type_name='MyRecord2')

    its_abstract = Mock(
        spec=['input_type', 'implementations'],
        input_type='AbstractRecord',
        implementations={
            'record1': its_record,
            'record2': its_record2})
    its_abstract.name = 'MyAbstractRecord'

    def setUp(self):
        self.v = Validator()

    def test_validate_scalar(self):
        node = DataNode(2, None, '/problem/1')
        node.its = TestValidator.its_int
        self.assertEqual(self.v.validate(node), True)

        node.value = 4
        self.assertEqual(self.v.validate(node), False)
        self.assertEqual(len(self.v.errors), 1)

    def test_validate_record(self):
        node = DataNode({'a1': 1, 'a2': 1})
        node.its = TestValidator.its_record
        self.assertEqual(self.v.validate(node), True)
        
        node = DataNode({'a1': 1, 'd': 2, 'e': 4})
        node.its = TestValidator.its_record
        self.assertEqual(self.v.validate(node), False)
        self.assertEqual(len(self.v.errors), 1)

    def test_validate_abstract(self):
        node = DataNode({'a1': 1, 'a2': 1, 'TYPE': 'record1'})
        node.its = TestValidator.its_abstract
        self.assertEqual(self.v.validate(node), True)

        node.value['TYPE'].value = 'record2'
        self.assertEqual(self.v.validate(node), False)

        del node.value['TYPE']
        self.assertEqual(self.v.validate(node), False)

    def test_validate(self):
        node = DataNode({'TYPE': 'record1', 'a1': 2, 'a2': 1})
        node.its=TestValidator.its_abstract
        self.assertEqual(self.v.validate(node), True)

        node = DataNode({'TYPE': 'record2', 'b': 2})
        node.its = TestValidator.its_abstract
        self.assertEqual(self.v.validate(node), True)

        node = DataNode({'TYPE': 'record1', 'a1': 5, 'a2': -1, 'e': 4, 'b': 'r'})
        node.its = TestValidator.its_abstract
        self.assertEqual(self.v.validate(node), False)
        self.assertEqual(len(self.v.errors), 3)

    def test_array(self):
        node = DataNode([0, 1, 1, 3])
        node.its = TestValidator.its_array
        self.assertEqual(self.v.validate(node), True)

        node = DataNode([0, 1, 1, 3,-1, 5])
        node.its = TestValidator.its_array
        self.assertEqual(self.v.validate(node), False)
        self.assertEqual(len(self.v.errors), 3)


