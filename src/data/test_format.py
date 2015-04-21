# -*- coding: utf-8 -*-
"""
Tests for format package.

@author: Tomas Krizek
"""

import unittest
from geomopcontext.data.format import FormatSpec, InputTypeSpec
from geomopcontext.validator.errors import *
from geomopcontext.data.selection import Selection


class TestFormatSpec(unittest.TestCase):
    """
    Basic rules include:
    Integer
    Double
    Bool
    String
    Selection
    FileName
    """

    def setUp(self):
        pass


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

    def test_its_integer(self):
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

    def test_validator_double(self):
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

    def test_validator_bool(self):
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

    def test_validator_string(self):
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

    def test_validator_filename(self):
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

    def test_validator_selection(self):
        data = {
                "id" : "f9756fb2f66076a1",
                "input_type" : "Selection",
                "name" : "PartTool",
                "full_name" : "PartTool",
                "description" : "Select the partitioning tool to use.",
                "values" : [{
                    "name" : "PETSc",
                    "description" : "Use PETSc interface to various partitioning tools."
                    },{
                    "name" : "METIS",
                    "description" : "Use direct interface to Metis." }]
                }
        its = InputTypeSpec(data)

        self.assertEqual(its.id, "f9756fb2f66076a1")
        self.assertEqual(its.input_type, "Selection")
        self.assertEqual(its.name, "PartTool")
        self.assertEqual(its.full_name, "PartTool")
        self.assertEqual(its.description,
            "Select the partitioning tool to use.")
        # TODO values


    def test_validator_array(self):
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

