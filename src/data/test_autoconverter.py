# -*- coding: utf-8 -*-
"""
Tests for auto-correct module

@author: Tomas Krizek
"""

import unittest
from unittest.mock import Mock

from . import autoconverter as ac
from .model import DataNode


class Testautoconvert(unittest.TestCase):
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
        self.assertEquals(expanded.value[0].value[0].value[0].path, \
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

        root = DataNode('str')
        expanded = ac._expand_reducible_to_key(root, its)

        self.assertEquals(expanded.get('/a').value, 'str')
        self.assertEquals(expanded.get('/a').path, '/a')


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

        root = DataNode('str')

        expanded = ac._expand_reducible_to_key(root, its)
        self.assertEqual(expanded.get('/a').value, 'str')
        self.assertEqual(expanded.get('/a').path, '/a')

    def test_autoconvert(self):
        its_record = Mock(
            spec=['input_type', 'keys', 'type_name'],
            input_type='Record',
            keys={
                'a': {
                    'default': {'type': 'obligatory'},
                    'type': Mock(
                        input_type='Integer')}},
            type_name='MyRecord',
            reducible_to_key='a')
        its_array = Mock(
            input_type='Array',
            subtype=Mock(
                input_type='Array',
                subtype=its_record))
        its = Mock(
            input_type='Record',
            keys={
                'path': {
                    'type': its_array
                }
            },
            type_name='Root')

        root = DataNode({'path': 2})
        converted = ac.autoconvert(root, its)
        print(converted.get('/path/0/0/a').value)
        print(root.get('/path').value)

        self.assertEqual(converted.get('/path/0/0/a').value, 2)

