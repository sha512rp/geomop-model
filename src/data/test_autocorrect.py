# -*- coding: utf-8 -*-
"""
Tests for auto-correct module

@author: Tomas Krizek
"""

import unittest
from unittest.mock import Mock
import geomopcontext.data.autocorrect as ac


class TestAutoCorrect(unittest.TestCase):
    def test_get_expected_array_dimension(self):
        its = Mock(
            input_type='Array',
            subtype=Mock(
                input_type='Array',
                subtype=Mock(
                    input_type='Array',
                    subtype=Mock(input_type='Integer')
                    )
                )
            )
        self.assertEquals(ac._get_expected_array_dimension(its), 3)

    def test_expand_value_to_array(self):
        class MyMock(object):
            pass


        node = MyMock()
        node.value = 1
        node.parent = MyMock()
        node.parent.path = '/path'
        node.path = '/path/key'
        node.name = 'key'

        expanded = ac._expand_value_to_array(node, 3)
        self.assertIsInstance(expanded.value, list)
        self.assertIsInstance(expanded.value[0].value, list)
        self.assertIsInstance(expanded.value[0].value[0].value, list)
        self.assertEquals(expanded.value[0].value[0].value[0].value, 1)
        self.assertEquals(expanded.value[0].value[0].value[0].path,
            '/path/key/0/0/0')

        self.assertEquals(
            expanded.value[0].value[0].value[0].parent.parent.parent.parent,
            node.parent)
