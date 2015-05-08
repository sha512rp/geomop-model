# -*- coding: utf-8 -*-
"""
Tests for auto-correct module

@author: Tomas Krizek
"""

import unittest
from unittest.mock import Mock
import geomopcontext.data.autocorrect as ac
from geomopcontext.data.con import DataNode


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
        node.value = MyMock()
        node.parent = MyMock()
        node.parent.path = '/path'
        node.path = '/path/key'
        node.name = 'key'

        expanded = ac._expand_value_to_array(node, 3)
        self.assertIsInstance(expanded.value, list)
        self.assertIsInstance(expanded.value[0].value, list)
        self.assertIsInstance(expanded.value[0].value[0].value, list)
        self.assertEquals(expanded.value[0].value[0].value[0].value, node.value)
        self.assertEquals(expanded.value[0].value[0].value[0].path,
            '/path/key/0/0/0')

        self.assertEquals(
            expanded.value[0].value[0].value[0].parent.parent.parent.parent,
            node.parent)


    def test_expand_record(self):
        its = Mock(
            spec=['input_type', 'keys', 'type_name'],
            input_type='Record',
            keys={
                'a': {
                    'default': {'type': 'obligatory'},
                    'type': Mock(
                        input_type='String')}},
            type_name='MyRecord',
            reducible_to_key='a')

        root = DataNode({'path': [1, 2, 3]})
        node = root.get('/path')
        node2 = root.get('/path/1')

        expanded = ac._expand_reducible_to_key(node, its)

        self.assertEquals(expanded.path, '/path')
        self.assertEquals(expanded.value['a'], node)
        self.assertEqual(expanded.get('a/1'), node2)


    def test_expand_abstractrecord(self):
        its_record = Mock(
            spec=['input_type', 'keys', 'type_name'],
            input_type='Record',
            keys={
                'a': {
                    'default': {'type': 'obligatory'},
                    'type': Mock(
                        input_type='String')}},
            type_name='MyRecord',
            reducible_to_key='a')

        its = Mock(
            input_type='AbstractRecord',
            default_descendant=its_record)

        root = DataNode({'path': [1, 2, 3]})
        node = root.get('/path')
        node2 = root.get('/path/1')

        expanded = ac._expand_reducible_to_key(node, its)

        self.assertEquals(expanded.path, '/path')
        self.assertEquals(expanded.value['a'], node)
        self.assertEqual(expanded.get('a/1'), node2)
