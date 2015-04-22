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

    def test_integer(self):
        data = {
                "id" : "151ce92dd201d44b",
                "input_type" : "Integer",
                "name" : "Integer",
                "full_name" : "Integer",
                "range" : [0, 3],
                "description": "description"
                }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "151ce92dd201d44b")
        self.assertEqual(its.input_type, "Integer")
        self.assertEqual(its.name, "Integer")
        self.assertEqual(its.full_name, "Integer")
        self.assertEqual(its.min, 0)
        self.assertEqual(its.max, 3)
        self.assertEqual(its.description, "description")

    def test_double(self):
        data = {
                "id" : "6b1c4ede475775aa",
                "input_type" : "Double",
                "name" : "Double",
                "full_name" : "Double",
                "range" : [0, 1.79769e+308],
                "description": "description"
                }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "6b1c4ede475775aa")
        self.assertEqual(its.input_type, "Double")
        self.assertEqual(its.name, "Double")
        self.assertEqual(its.full_name, "Double")
        self.assertEqual(its.min, 0)
        self.assertEqual(its.max, 1.79769e+308)
        self.assertEqual(its.description, "description")

    def test_bool(self):
        data = {
                "id" : "282546d52edd4",
                "input_type" : "Bool",
                "name" : "Bool",
                "full_name" : "Bool",
                "description": "description"
                }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "282546d52edd4")
        self.assertEqual(its.input_type, "Bool")
        self.assertEqual(its.name, "Bool")
        self.assertEqual(its.full_name, "Bool")
        self.assertEqual(its.description, "description")

    def test_string(self):
        data = {
                "id" : "29b5533100b6f60f",
                "input_type" : "String",
                "name" : "String",
                "full_name" : "String",
                "description": "description"
                }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "29b5533100b6f60f")
        self.assertEqual(its.input_type, "String")
        self.assertEqual(its.name, "String")
        self.assertEqual(its.full_name, "String")
        self.assertEqual(its.description, "description")

    def test_filename(self):
        data = {
                "id" : "89a808b8e9515bf8",
                "input_type" : "FileName",
                "name" : "FileName_input",
                "full_name" : "FileName_input",
                "file_mode" : "input",
                "description": "description"
                }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "89a808b8e9515bf8")
        self.assertEqual(its.input_type, "FileName")
        self.assertEqual(its.name, "FileName_input")
        self.assertEqual(its.full_name, "FileName_input")
        self.assertEqual(its.file_mode, "input")
        self.assertEqual(its.description, "description")

    def test_selection(self):
        data = {
                "id" : "f9756fb2f66076a1",
                "input_type" : "Selection",
                "name" : "PartTool",
                "full_name" : "PartTool",
                "description" : "description",
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
        self.assertEqual(its.name, "PartTool")
        self.assertEqual(its.full_name, "PartTool")
        self.assertEqual(its.description, "description")
        self.assertEqual(its.values.PETSc.description, "PETSc description")
        self.assertEqual(its.values.METIS.description, "METIS description")

    def test_array(self):
        data = {
                "id" : "eee3033466b9ffa2",
                "input_type" : "Array",
                "range" : [0, 4294967295],
                "subtype" : "6b1c4ede475775aa",
                "description": "description"
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
                "description" : "Definition of region of elements.",
                "keys" : [
                { "key" : "name",
                "description" : "Label (name) of the region.",
                "default" : { "type" : "obligatory",
                "value" : "OBLIGATORY" },
                "type" : "29b5533100b6f60f"
                },
                { "key" : "id",
                "description" : "The ID of the region",
                "default" : { "type" : "obligatory",
                "value" : "OBLIGATORY" },
                "type" : "151ce92d5201d44f"
                },
                { "key" : "element_list",
                "description" : "list of elements",
                "default" : { "type" : "optional",
                "value" : "OPTIONAL" },
                "type" : "ccc88a2172d23cc3"
                }]
            }
            its = InputTypeSpec(data)

            self.assertEqual(its.id, "b9614d55a6c3462e")
            self.assertEqual(its.input_type, "Record")
            # self.assertEqual(its.type_name, "Region")
            # self.assertEqual(its.type_full_name, "Region")
            self.assertEqual(its.description, "Definition of region of elements.")
            # self.assertEqual(its.keys.name, 0)
            # self.assertEqual(its.max, 4294967295)
            # self.assertEqual(its.subtype, "6b1c4ede475775aa")


class TestKeySet(unittest.TestCase):
    
    def setUp(self):
        data = [{
                "name" : "PETSc",
                "description" : "PETSc description"
            },{
                "name" : "METIS",
                "description" : "METIS description"
            }]
        self.values = KeySet(data)


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

