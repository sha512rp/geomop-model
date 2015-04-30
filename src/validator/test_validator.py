# -*- coding: utf-8 -*-
"""
Tests for validator

@author: Tomas Krizek
"""

import unittest
from unittest.mock import Mock

from geomopcontext.validator.validator import *
from geomopcontext.validator.errors import *
from geomopcontext.data.format import FormatSpec

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
        node = Mock(
            its=TestValidator.its_int,
            value=2,
            path='/problem/1/number')
        self.assertEqual(self.v.validate(node), True)

        node.value = 4
        self.assertEqual(self.v.validate(node), False)
        self.assertEqual(len(self.v.errors), 1)

    def test_validate_record(self):
        node = Mock(
            its=TestValidator.its_record, 
            value={
                'a1': Mock(value=1),
                'a2': Mock(value=1)},
            path='/record')
        self.assertEqual(self.v.validate(node), True)

        node.value = {
            'a1': Mock(value=1),
            'd': Mock(value=2),
            'e': Mock(value=4)}
        self.assertEqual(self.v.validate(node), False)
        self.assertEqual(len(self.v.errors), 2)

    def test_validate_abstract(self):
        node = Mock(
            spec=['its', 'value', 'path'],
            its=TestValidator.its_abstract,
            value={
                'a1': Mock(value=1),
                'a2': Mock(value=1),
                'TYPE': Mock(value='record1')},
            path='/abstract')
        self.assertEqual(self.v.validate(node), True)

        node.value['TYPE'].value = 'record2'
        self.assertEqual(self.v.validate(node), False)

        del node.value['TYPE']
        self.assertEqual(self.v.validate(node), False)

    def test_validate(self):
        node = Mock(
            value={
                'TYPE': Mock(value='record1', path='/r/TYPE'),
                'a1': Mock(value=2, path='/r/a1'),
                'a2': Mock(value=1, path='/r/a2')},
            its=TestValidator.its_abstract,
            path='/r')
        self.assertEqual(self.v.validate(node), True)

        node = Mock(
            value={
                'TYPE': Mock(value='record2', path='/r/TYPE'),
                'b': Mock(value=2, path='/r/b')},
            its=TestValidator.its_abstract,
            path='/r')
        self.assertEqual(self.v.validate(node), True)

        node = Mock(
            value={
                'TYPE': Mock(value='record1', path='/r/TYPE'), 
                'a1': Mock(value=5, path='/r/a1'), 
                'a2': Mock(value=-1, path='/r/a2'), 
                'e': Mock(value=4, path='/r/e'),
                'b': Mock(value='r', path='/r/b')},
            its=TestValidator.its_abstract,
            path='/r')
        self.assertEqual(self.v.validate(node), False)
        self.assertEqual(len(self.v.errors), 4)

    def test_array(self):
        node = Mock(
            value=[
                Mock(value=0),
                Mock(value=1),
                Mock(value=1),
                Mock(value=3)],
            its=TestValidator.its_array)
        self.assertEqual(self.v.validate(node), True)

        node.value.append(Mock(value=-1))
        node.value.append(Mock(value=5))

        self.assertEqual(self.v.validate(node), False)
        self.assertEqual(len(self.v.errors), 3)


