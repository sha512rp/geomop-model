# -*- coding: utf-8 -*-
"""
Tests for rules

@author: Tomas Krizek
"""

import unittest
import geomopcontext.validator.rules as rules
from geomopcontext.validator.errors import *
from geomopcontext.data.selection import Selection

class TestBasicRules(unittest.TestCase):
    """
    Basic rules include:
    Integer
    Double
    Bool
    String

    Record
    AbstractRecord
    Selection
    Array

    FileName
    Null?
    """

    def setUp(self):
        pass

    def test_check_integer(self):
        """
            check_integer(val)
            check_integer(val, min=a, max=b)
        """
        self.assertEquals(rules.check_integer(3), True);
        self.assertEquals(rules.check_integer(-2), True);

        with self.assertRaises(TypeError):
            rules.check_integer(2.5);
            rules.check_integer("3");
            rules.check_integer({});
            rules.check_integer([]);

        self.assertEquals(rules.check_integer(3, min=0, max=3), True);
        self.assertEquals(rules.check_integer(2, min=0, max=3), True);
        self.assertEquals(rules.check_integer(0, min=0, max=3), True);

        with self.assertRaises(ValueTooSmall):
            rules.check_integer(-1, min=0, max=3);

        with self.assertRaises(ValueTooBig):
            rules.check_integer(5, min=0, max=3);

    def test_check_double(self):
        """
            check_double(val)
            check_double(val, min=a, max=b)
        """
        self.assertEquals(rules.check_double(3.14), True);
        self.assertEquals(rules.check_double(-2), True);        # accepts int

        with self.assertRaises(TypeError):
            rules.check_double("3.14")
            rules.check_double({});
            rules.check_double([]);

        self.assertEquals(rules.check_double(3.14, min=0, max=3.14), True);
        self.assertEquals(rules.check_double(2.5, min=0, max=3.14), True);
        self.assertEquals(rules.check_double(0, min=0, max=3.14), True);

        with self.assertRaises(ValueTooSmall):
            rules.check_double(-1.3, min=0, max=3.14);

        with self.assertRaises(ValueTooBig):
            rules.check_double(5, min=0, max=3.14);

    def test_check_bool(self):
        """
            check_bool(val)
        """
        self.assertEquals(rules.check_bool(True), True);
        self.assertEquals(rules.check_bool(False), True);

        with self.assertRaises(TypeError):
            rules.check_bool(0);
            rules.check_bool(1);
            rules.check_bool("1");
            rules.check_bool("false");
            rules.check_bool({});
            rules.check_bool([]);

    def test_check_string(self):
        """
            check_string(val)
        """
        self.assertEquals(rules.check_string("abc"), True);

        with self.assertRaises(TypeError):
            rules.check_string(0);
            rules.check_string({});
            rules.check_string([]);

    def test_check_selection(self):
        """
            check_selection(selection, value)
        """

        options = {
                    'any_neighboring': 0,\
                    'any_wight_lower_dim_cuts': 1,\
                    'same_dimension_neghboring': 2 \
        }
        GraphType = Selection('GraphType', options)
        MySelection = Selection('MySelection', {'a': 44,})

        self.assertEquals(rules.check_selection(GraphType,
            'any_wight_lower_dim_cuts'), True);

        #with self.assertRaises(InvalidOption):
        rules.check_selection(MySelection,
            'any_wight_lower_dim_cuts')

if __name__ == '__main__':
    unittest.main()
