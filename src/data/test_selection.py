# -*- coding: utf-8 -*-
"""
Tests for selection

@author: Tomas Krizek
"""

import unittest
from geomopcontext.data.selection import Selection


class TestSelection(unittest.TestCase):
    """
        Test generating and using selections.
    """

    def setUp(self):
        options = {
                    'any_neighboring': 0,\
                    'any_wight_lower_dim_cuts': 1,\
                    'same_dimension_neghboring': 2 \
        }

        Selection('GraphType', options)

        options['any_wight_lower_dim_cuts'] = 6  # shouldn't be effective

    def test_selection_exists(self):
        GraphType = Selection.selection('GraphType')
        self.assertEqual(GraphType.to_str(2), 'same_dimension_neghboring')
        self.assertEqual(GraphType.has('any_neighboring'), True)
        self.assertEqual(GraphType.has('invalid'), False)

        with self.assertRaises(KeyError):
            GraphType.to_str(3)
            GraphType.to_int('invalid')

    def test_selection_kwargs(self):
        full_name = "My Awesome Selection"
        description = "The best Selection of them all - MySelection!"
        options = {'a': 1}
        invalid_arg = "invalid"

        MySelection = Selection('MySelection', options, 
            full_name=full_name, description=description, 
            invalid_arg=invalid_arg)

        self.assertEqual(MySelection.full_name, full_name)
        self.assertEqual(MySelection.description, description)

        with self.assertRaises(AttributeError):
            MySelection.invalid_arg

