# -*- coding: utf-8 -*-
"""
Tests for rules

@author: Tomas Krizek
"""

import unittest
import rules
from errors import *

class TestBasicRules(unittest.TestCase):
    """
    Basic rules include:
    Integer
    Double

    Record
    AbstractRecord
    Selection
    Array
    String
    FileName
    Bool

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
            rules.check_double("3.14");
            rules.check_double({});
            rules.check_double([]);

        self.assertEquals(rules.check_double(3.14, min=0, max=3.14), True);
        self.assertEquals(rules.check_double(2.5, min=0, max=3.14), True);
        self.assertEquals(rules.check_double(0, min=0, max=3.14), True);

        with self.assertRaises(ValueTooSmall):
            rules.check_double(-1.3, min=0, max=3.14);

        with self.assertRaises(ValueTooBig):
            rules.check_double(5, min=0, max=3.14);


if __name__ == '__main__':
    unittest.main()
