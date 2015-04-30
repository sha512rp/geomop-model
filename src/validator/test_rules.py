# -*- coding: utf-8 -*-
"""
Tests for rules

@author: Tomas Krizek
"""

import unittest
from unittest.mock import Mock
import geomopcontext.validator.rules as rules
from geomopcontext.validator.errors import *
from geomopcontext.data.format import InputTypeSpec

class TestBasicRules(unittest.TestCase):
    """
    Basic rules include:
    Integer
    Double
    Bool
    String
    Selection
    FileName
    """

    def test_check_integer(self):
        its = Mock(min=0, max=3)
        its_inf = Mock(min=float('-inf'), max=float('inf'))

        self.assertEquals(rules.check_integer(3, its_inf), True);
        self.assertEquals(rules.check_integer(-2, its_inf), True);

        with self.assertRaises(ValidationTypeError):
            rules.check_integer(2.5, its);
            rules.check_integer("3", its);
            rules.check_integer({}, its);
            rules.check_integer([], its);

        self.assertEquals(rules.check_integer(3, its), True);
        self.assertEquals(rules.check_integer(2, its), True);
        self.assertEquals(rules.check_integer(0, its), True);

        with self.assertRaises(ValueTooSmall):
            rules.check_integer(-1, its);

        with self.assertRaises(ValueTooBig):
            rules.check_integer(5, its);

    def test_check_double(self):
        its = Mock(min=0, max=3.14)
        its_inf = Mock(min=float('-inf'), max=float('inf'))

        self.assertEquals(rules.check_double(3.14, its_inf), True);
        self.assertEquals(rules.check_double(-2, its_inf), True);        # accepts int

        with self.assertRaises(ValidationTypeError):
            rules.check_double("3.14", its)
            rules.check_double({}, its);
            rules.check_double([], its);

        self.assertEquals(rules.check_double(3.14, its), True);
        self.assertEquals(rules.check_double(2.5, its), True);
        self.assertEquals(rules.check_double(0, its), True);

        with self.assertRaises(ValueTooSmall):
            rules.check_double(-1.3, its);

        with self.assertRaises(ValueTooBig):
            rules.check_double(5, its);

    def test_check_bool(self):
        its = Mock()
        self.assertEquals(rules.check_bool(True, its), True);
        self.assertEquals(rules.check_bool(False, its), True);

        with self.assertRaises(ValidationTypeError):
            rules.check_bool(0, its);
            rules.check_bool(1, its);
            rules.check_bool("1", its);
            rules.check_bool("false", its);
            rules.check_bool({}, its);
            rules.check_bool([], its);

    def test_check_string(self):
        its = Mock()
        self.assertEquals(rules.check_string("abc", its), True);

        with self.assertRaises(ValidationTypeError):
            rules.check_string(0, its);
            rules.check_string({}, its);
            rules.check_string([], its);

    def test_check_selection(self):
        its = Mock(values={'a': 1, 'b': 2, 'c': 3})
        its.name = 'MySelection'

        self.assertEquals(rules.check_selection('a', its), True)
        self.assertEquals(rules.check_selection('b', its), True)
        self.assertEquals(rules.check_selection('c', its), True)

        with self.assertRaises(InvalidOption):
            self.assertEquals(rules.check_selection('d', its), True)

    def test_check_filename(self):
        its = Mock()
        self.assertEquals(rules.check_filename("abc", its), True);

        with self.assertRaises(ValidationTypeError):
            rules.check_filename(0, its);
            rules.check_filename({}, its);
            rules.check_filename([], its);

    def test_check_array(self):
        its = Mock(min=1, max=5)
        its_inf = Mock(min=0, max=float('inf'))
        self.assertEquals(rules.check_array([], its_inf), True);
        self.assertEquals(rules.check_array([None]*2, its), True);
        self.assertEquals(rules.check_array([None]*1, its), True);
        self.assertEquals(rules.check_array([None]*5, its), True);

        with self.assertRaises(ValidationTypeError):
            rules.check_array(None, its)

        with self.assertRaises(NotEnoughItems):
            rules.check_array([], its);

        with self.assertRaises(TooManyItems):
            rules.check_array([None]*6, its);

    def test_check_record_key(self):
        keys = {
            'a1': {'default': {'type': 'obligatory'}},
            'a2': {'default': {'type': 'obligatory'}},
            'b': {'default': {'type': 'value at declaration'}},
            'c': {'default': {'type': 'value at read time'}},
            'd': {'default': {'type': 'optional'}}
        }
        its = Mock(keys=keys, type_name='MyRecord')

        self.assertEquals(rules.check_record_key({'a1': None}, 'a1', its), True)
        self.assertEquals(rules.check_record_key({'a1': None}, 'b', its), True)
        self.assertEquals(rules.check_record_key({'a1': None}, 'c', its), True)
        self.assertEquals(rules.check_record_key({'a1': None}, 'd', its), True)

        with self.assertRaises(MissingKey):
            rules.check_record_key({'a1': None}, 'a2', its)

        with self.assertRaises(UnknownKey):
            rules.check_record_key({'unknown': None}, 'unknown', its)

        with self.assertRaises(ValidationTypeError):
            rules.check_record_key([], 'a', its);


    def test_check_abstractrecord(self):
        type1 = Mock(type_name='type1')
        type2 = Mock(type_name='type2')
        type3 = Mock(type_name='type3')
        its = Mock(default_descendant=type1, implementations={
            'type1': type1,'type2': type2, 'type3': type3})
        its.name = 'MyAbstractRecord'
        its_no_default = Mock(spec=['implementations'], 
            implementations={'type1': type1, 'type2': type2, 'type3': type3})

        self.assertEqual(rules.get_abstractrecord_type(
            {'TYPE': Mock(value='type2')}, its), type2)
        self.assertEqual(rules.get_abstractrecord_type({}, its), type1)

        self.assertEqual(rules.get_abstractrecord_type(
            {'TYPE': Mock(value='type3')}, its_no_default), type3)
        with self.assertRaises(MissingAbstractRecordType):
            rules.get_abstractrecord_type({}, its_no_default)

        with self.assertRaises(InvalidAbstractRecordType):
            rules.get_abstractrecord_type(
                {'TYPE': Mock(value='invalid')}, its)

        with self.assertRaises(ValidationTypeError):
            rules.get_abstractrecord_type([], its);

