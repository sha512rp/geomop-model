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
        its = Mock(values=Mock(keys=Mock(return_value=['a', 'b', 'c'])))
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
        self.assertEquals(rules.check_array([1, 2], its), True);
        self.assertEquals(rules.check_array([1], its), True);
        self.assertEquals(rules.check_array([1, 2, 3, 4, 5], its), True);

        with self.assertRaises(ValidationTypeError):
            rules.check_array(23, its)

        with self.assertRaises(NotEnoughItems):
            rules.check_array([], its);

        with self.assertRaises(TooManyItems):
            rules.check_array([1, 2, 3, 4, 5, 6], its);


class TestRuleParser(unittest.TestCase):
    pass


    # def test_rule_parser_selection(self):
    #     """
    #         single rule parse test
    #     """
    #     rules = [{
    #             "id" : "f9756fb2f66076a1",
    #             "input_type" : "Selection",
    #             "name" : "PartTool",
    #             "full_name" : "PartTool",
    #             "description" : "Select the partitioning tool to use.",
    #             "values" : [
    #             { "value" : "0",
    #              "name" : "PETSc",
    #             "description" : "Use PETSc interface to various partitioning tools." },
    #             { "value" : "1",
    #              "name" : "METIS",
    #             "description" : "Use direct interface to Metis." }]
    #             }]
    #     self.rule_parser.parse(rules)
    #     self.rule_parser.rules['f9756fb2f66076a1'] = 


if __name__ == '__main__':
    unittest.main()
