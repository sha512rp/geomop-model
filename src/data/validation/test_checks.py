# -*- coding: utf-8 -*-
"""
GeoMop Model

Tests for basic validation checks.

@author: Tomas Krizek
"""

import unittest
from unittest.mock import Mock

from . import checks, errors
from ..format import InputTypeSpec


class TestBasicChecks(unittest.TestCase):
    """
    Basic checks include:
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

        self.assertEquals(checks.check_integer(3, its_inf), True);
        self.assertEquals(checks.check_integer(-2, its_inf), True);

        with self.assertRaises(errors.ValidationTypeError):
            checks.check_integer(2.5, its);
            checks.check_integer("3", its);
            checks.check_integer({}, its);
            checks.check_integer([], its);

        self.assertEquals(checks.check_integer(3, its), True);
        self.assertEquals(checks.check_integer(2, its), True);
        self.assertEquals(checks.check_integer(0, its), True);

        with self.assertRaises(errors.ValueTooSmall):
            checks.check_integer(-1, its);

        with self.assertRaises(errors.ValueTooBig):
            checks.check_integer(5, its);

    def test_check_double(self):
        its = Mock(min=0, max=3.14)
        its_inf = Mock(min=float('-inf'), max=float('inf'))

        self.assertEquals(checks.check_double(3.14, its_inf), True);
        self.assertEquals(checks.check_double(-2, its_inf), True);        # accepts int

        with self.assertRaises(errors.ValidationTypeError):
            checks.check_double("3.14", its)
            checks.check_double({}, its);
            checks.check_double([], its);

        self.assertEquals(checks.check_double(3.14, its), True);
        self.assertEquals(checks.check_double(2.5, its), True);
        self.assertEquals(checks.check_double(0, its), True);

        with self.assertRaises(errors.ValueTooSmall):
            checks.check_double(-1.3, its);

        with self.assertRaises(errors.ValueTooBig):
            checks.check_double(5, its);

    def test_check_bool(self):
        its = Mock()
        self.assertEquals(checks.check_bool(True, its), True);
        self.assertEquals(checks.check_bool(False, its), True);

        with self.assertRaises(errors.ValidationTypeError):
            checks.check_bool(0, its);
            checks.check_bool(1, its);
            checks.check_bool("1", its);
            checks.check_bool("false", its);
            checks.check_bool({}, its);
            checks.check_bool([], its);

    def test_check_string(self):
        its = Mock()
        self.assertEquals(checks.check_string("abc", its), True);

        with self.assertRaises(errors.ValidationTypeError):
            checks.check_string(0, its);
            checks.check_string({}, its);
            checks.check_string([], its);

    def test_check_selection(self):
        its = Mock(values={'a': 1, 'b': 2, 'c': 3})
        its.name = 'MySelection'

        self.assertEquals(checks.check_selection('a', its), True)
        self.assertEquals(checks.check_selection('b', its), True)
        self.assertEquals(checks.check_selection('c', its), True)

        with self.assertRaises(errors.InvalidOption):
            self.assertEquals(checks.check_selection('d', its), True)

    def test_check_filename(self):
        its = Mock()
        self.assertEquals(checks.check_filename("abc", its), True);

        with self.assertRaises(errors.ValidationTypeError):
            checks.check_filename(0, its);
            checks.check_filename({}, its);
            checks.check_filename([], its);

    def test_check_array(self):
        its = Mock(min=1, max=5)
        its_inf = Mock(min=0, max=float('inf'))
        self.assertEquals(checks.check_array([], its_inf), True);
        self.assertEquals(checks.check_array([None]*2, its), True);
        self.assertEquals(checks.check_array([None]*1, its), True);
        self.assertEquals(checks.check_array([None]*5, its), True);

        with self.assertRaises(errors.ValidationTypeError):
            checks.check_array(None, its)

        with self.assertRaises(errors.NotEnoughItems):
            checks.check_array([], its);

        with self.assertRaises(errors.TooManyItems):
            checks.check_array([None]*6, its);

    def test_check_record_key(self):
        keys = {
            'a1': {'default': {'type': 'obligatory'}},
            'a2': {'default': {'type': 'obligatory'}},
            'b': {'default': {'type': 'value at declaration'}},
            'c': {'default': {'type': 'value at read time'}},
            'd': {'default': {'type': 'optional'}}
        }
        its = Mock(keys=keys, type_name='MyRecord')

        self.assertEquals(checks.check_record_key({'a1': None}, 'a1', its), True)
        self.assertEquals(checks.check_record_key({'a1': None}, 'b', its), True)
        self.assertEquals(checks.check_record_key({'a1': None}, 'c', its), True)
        self.assertEquals(checks.check_record_key({'a1': None}, 'd', its), True)
        self.assertEqual(
            checks.check_record_key({'unknown': None}, 'unknown', its),
            True)

        with self.assertRaises(errors.MissingKey):
            checks.check_record_key({'a1': None}, 'a2', its)


        with self.assertRaises(errors.ValidationTypeError):
            checks.check_record_key([], 'a', its);


    def test_check_abstractrecord(self):
        type1 = Mock(type_name='type1')
        type2 = Mock(type_name='type2')
        type3 = Mock(type_name='type3')
        its = Mock(default_descendant=type1, implementations={
            'type1': type1,'type2': type2, 'type3': type3})
        its.name = 'MyAbstractRecord'
        its_no_default = Mock(spec=['implementations'], 
            implementations={'type1': type1, 'type2': type2, 'type3': type3})

        self.assertEqual(checks.get_abstractrecord_type(
            {'TYPE': Mock(value='type2')}, its), type2)
        self.assertEqual(checks.get_abstractrecord_type({}, its), type1)

        self.assertEqual(checks.get_abstractrecord_type(
            {'TYPE': Mock(value='type3')}, its_no_default), type3)
        with self.assertRaises(errors.MissingAbstractRecordType):
            checks.get_abstractrecord_type({}, its_no_default)

        with self.assertRaises(errors.InvalidAbstractRecordType):
            checks.get_abstractrecord_type(
                {'TYPE': Mock(value='invalid')}, its)

