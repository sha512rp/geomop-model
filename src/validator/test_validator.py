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

    def test_validate_simple_check(self):
        its = Mock(input_type='Integer', min=0, max=3)
        node = Mock(its=its, value=2, path='/problem/1/number')
        self.assertEqual(validate_node(node).valid, True)

        node.value = 4
        result = validate_node(node)
        self.assertEqual(result.valid, False)
        self.assertEqual(len(result.errors), 1)

    def test_validate_record(self):
        its = Mock(
            input_type='Record',
            keys={
                'a1': {'default': {'type': 'obligatory'}},
                'a2': {'default': {'type': 'obligatory'}},
                'b': {'default': {'type': 'value at declaration'}},
                'c': {'default': {'type': 'value at read time'}},
                'd': {'default': {'type': 'optional'}}
        })
        its.name = 'MyRecord'
        node=Mock(its=its, value={'a1': 1, 'a2': 2}, path='/record')
        self.assertEqual(validate_node(node).valid, True)

        node.value = {'a1': 1, 'd': 2, 'e': 4}
        result = validate_node(node)
        self.assertEqual(result.valid, False)
        self.assertEqual(len(result.errors), 2)

    def test_validate_abstract(self):
        its_record1 = Mock(
            input_type='Record',
            keys={'a': {'default': {'type': 'obligatory'}}})
        its_record1.name = 'MyRecord1'
        its_record2 = Mock(
            input_type='Record',
            keys={'b': {'default': {'type': 'obligatory'}}})
        its_record2.name = 'MyRecord2'
        its = Mock(
            spec=['input_type', 'implementations'],
            input_type='AbstractRecord',
            implementations={
                'record1': its_record1,
                'record2': its_record2
        })
        its.name = 'MyAbstractRecord'
        node=Mock(
            its=its,
            value={'a': 1, 'TYPE': 'record1'},
            path='/abstract')
        self.assertEqual(validate_node(node).valid, True)

        node.value['TYPE'] = 'record2'
        self.assertEqual(validate_node(node).valid, False)

        del node.value['TYPE']
        self.assertEqual(validate_node(node).valid, False)


class TestValidationResult(unittest.TestCase):

    def test_report(self):
        result = ValidationResult()
        self.assertEqual(result.valid, True)

        result.report(Exception())
        self.assertEqual(result.valid, False)

