# -*- coding: utf-8 -*-
"""
Tests for format package.

@author: Tomas Krizek
"""

import unittest
from geomopcontext.data.format import *


class TestFormatSpec(unittest.TestCase):

    def setUp(self):
        data = [
            {
            "id" : "cde734cca8c6d536",
            "input_type" : "Record",
            "type_name" : "Root",
            "type_full_name" : "Root",

            "description" : "Root record of JSON input for Flow123d.",
            "keys" : [
            { "key" : "problem",
            "description" : "Simulation problem to be solved.",
            "default" : { "type" : "obligatory",
            "value" : "OBLIGATORY" },
            "type" : "1b71c90f49db780"
            },
            { "key" : "pause_after_run",
            "description" : "If true, the program will wait for key press before it terminates.",
            "default" : { "type" : "value at declaration",
            "value" : "false" },
            "type" : "282546d52edd4"
            }]
        }]


class TestInputTypeSpec(unittest.TestCase):
    """
    ITS include:
    Integer
    Double
    Bool
    String
    Selection
    FileName
    Array

    not implemented yet:
    Record
    AbstractRecord
    """

    def test_optional_params(self):
        data = {
            "id" : "151ce92dd201d44b",
            "input_type" : "",
            "name" : "Integer",
            "full_name" : "Integer",
            "description": "description"
        }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "151ce92dd201d44b")
        self.assertEqual(its.input_type, "")
        self.assertEqual(its.name, "Integer")
        self.assertEqual(its.full_name, "Integer")
        self.assertEqual(its.description, "description")

    def test_integer(self):
        data = {
                "id" : "151ce92dd201d44b",
                "input_type" : "Integer",
                "range" : [0, 3]
                }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "151ce92dd201d44b")
        self.assertEqual(its.input_type, "Integer")
        self.assertEqual(its.min, 0)
        self.assertEqual(its.max, 3)

    def test_double(self):
        data = {
                "id" : "6b1c4ede475775aa",
                "input_type" : "Double",
                "range" : [0, 1.79769e+308],
                }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "6b1c4ede475775aa")
        self.assertEqual(its.input_type, "Double")
        self.assertEqual(its.min, 0)
        self.assertEqual(its.max, 1.79769e+308)

    def test_bool(self):
        data = {
                "id" : "282546d52edd4",
                "input_type" : "Bool"
                }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "282546d52edd4")
        self.assertEqual(its.input_type, "Bool")

    def test_string(self):
        data = {
                "id" : "29b5533100b6f60f",
                "input_type" : "String"
                }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "29b5533100b6f60f")
        self.assertEqual(its.input_type, "String")

    def test_filename(self):
        data = {
                "id" : "89a808b8e9515bf8",
                "input_type" : "FileName",
                "file_mode" : "input"
                }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "89a808b8e9515bf8")
        self.assertEqual(its.input_type, "FileName")
        self.assertEqual(its.file_mode, "input")

    def test_selection(self):
        data = {
                "id" : "f9756fb2f66076a1",
                "input_type" : "Selection",
                "values" : [{
                    "name" : "PETSc",
                    "description" : "PETSc description"
                    },{
                    "name" : "METIS",
                    "description" : "METIS description" }]
                }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "f9756fb2f66076a1")
        self.assertEqual(its.input_type, "Selection")
        self.assertEqual(its.values.PETSc.description, "PETSc description")
        self.assertEqual(its.values.METIS.description, "METIS description")

    def test_array(self):
        data = {
                "id" : "eee3033466b9ffa2",
                "input_type" : "Array",
                "range" : [0, 4294967295],
                "subtype" : "6b1c4ede475775aa",
                }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "eee3033466b9ffa2")
        self.assertEqual(its.input_type, "Array")
        self.assertEqual(its.min, 0)
        self.assertEqual(its.max, 4294967295)
        self.assertEqual(its.subtype, "6b1c4ede475775aa")

    def test_record(self):
        data = {
            "id" : "b9614d55a6c3462e",
            "input_type" : "Record",
            "type_name" : "Region",
            "type_full_name" : "Region",
            "keys" : [
            { "key" : "name",
            "default" : { "type" : "obligatory",
            "value" : "OBLIGATORY" },
            "type" : "29b5533100b6f60f"
            }]
        }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "b9614d55a6c3462e")
        self.assertEqual(its.input_type, "Record")
        self.assertEqual(its.type_name, "Region")
        self.assertEqual(its.type_full_name, "Region")
        self.assertEqual(its.keys.name.default.type, 'obligatory')
        self.assertEqual(its.keys.name.default.value, 'OBLIGATORY')
        self.assertEqual(its.keys.name.type, '29b5533100b6f60f')

    def test_abstract_record(self):
        data = {
            "id" : "89b3f44e8ecaec1b",
            "input_type" : "AbstractRecord",
            "default_descendant": "59d2b27373f5effe",
            "implementations" : ["59d2b27373f5effe"]
        }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "89b3f44e8ecaec1b")
        self.assertEqual(its.input_type, "AbstractRecord")
        self.assertEqual(its.default_descendant, '59d2b27373f5effe')
        self.assertEqual(its.implementations, ["59d2b27373f5effe"])


class TestKeySet(unittest.TestCase):
    
    def setUp(self):
        data = [{
                "name" : "PETSc",
                "description" : "PETSc description"
            },{
                "name" : "METIS",
                "description" : "METIS description"
            }]
        self.values = KeySet(data, key_label='name')

    def test_dot_notation(self):
        self.assertEqual(self.values.PETSc.description, "PETSc description")
        self.assertEqual(self.values.METIS.description, "METIS description")

    def test_length(self):
        self.assertEqual(len(self.values), 2)

    def test_iteration(self):
        names = ["PETSc", "METIS"]
        for item in self.values:
            self.assertIn(item.name, names)

    def test_contains(self):
        names = ["PETSc", "METIS"]
        for name in names:
            self.assertIn(name, self.values)


class TestObjectView(unittest.TestCase):
    
    def test_dot_notation(self):
        data = {
            'computer1': {
                'name': 'sharp-pc',
                'equipment': {
                    'mouse': 'Logitech G500'
                },
                'components': {
                    'cpu': {
                        'brand': 'Intel',
                        'name': 'Intel i5',
                        'freq': '3.2 Ghz'
                    },
                    'gpu': 'ATI Radeon 880M'
                }
            },
            'computer2': {
                'name': 'old-pc'
            }
        }
        computers = ObjectView(data)
        self.assertEqual(computers.computer1.name, 'sharp-pc')
        self.assertEqual(computers.computer1.components.cpu.brand, 'Intel')
        self.assertEqual(computers.computer2.name, 'old-pc')

