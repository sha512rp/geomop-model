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
        self.values = [  {
                        "value" : "0",
                        "name" : "any_neighboring",
                        "description" : "Add edge for any pair of neighboring elements."
                    }, {
                        "value" : "1",
                        "name" : "any_wight_lower_dim_cuts",
                        "description" : "Same as before and assign higher weight to cuts of lower dimension in order to make them stick to one face."
                    }, {
                        "value" : "2",
                        "name" : "same_dimension_neghboring",
                        "description" : "Add edge for any pair of neighboring elements of same dimension (bad for matrix multiply)."
                }]

        self.selections = {}
        self.selections['GraphType'] = Selection('GraphType', self.values)

    def test_selection_exists(self):
        GraphType = self.selections['GraphType']
        self.assertEqual(GraphType.to_str(2), 'same_dimension_neghboring')
        self.assertEqual(GraphType.has('any_neighboring'), True)
        self.assertEqual(GraphType.has('invalid'), False)

        with self.assertRaises(KeyError):
            GraphType.to_str(3)

    def test_selection_kwargs(self):
        full_name = "My Awesome Selection"
        description = "The best Selection of them all - MySelection!"
        invalid_arg = "invalid"

        MySelection = Selection('MySelection', self.values, 
            full_name=full_name, description=description, 
            invalid_arg=invalid_arg)

        self.assertEqual(MySelection.full_name, full_name)
        self.assertEqual(MySelection.description, description)

        with self.assertRaises(AttributeError):
            MySelection.invalid_arg

