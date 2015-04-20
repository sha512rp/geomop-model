# -*- coding: utf-8 -*-
"""
Tests for validator

@author: Tomas Krizek
"""

import unittest

from geomopcontext.validator.validator import Validator, ValidationResult, Severity
from geomopcontext.validator.errors import *

class TestValidator(unittest.TestCase):

    def test_validator_integer(self):
        rules = [{
                "id" : "151ce92dd201d44b",
                "input_type" : "Integer",
                "name" : "Integer",
                "full_name" : "Integer",
                "range" : [0, 3]
                }]
        validator = Validator(rules)

        self.assertEqual(validator.validate(0).valid, True)
        self.assertEqual(validator.validate(2).valid, True)
        self.assertEqual(validator.validate(3).valid, True)

        result = validator.validate(4)
        self.assertEqual(result.valid, False)
        self.assertIsInstance(result.messages[0]['exception'], ValueTooBig)

        result = validator.validate(-1)
        self.assertEqual(result.valid, False)
        self.assertIsInstance(result.messages[0]['exception'], ValueTooSmall)

        result = validator.validate('asd')
        self.assertEqual(result.valid, False)
        self.assertIsInstance(result.messages[0]['exception'], ValidationTypeError)

    def test_validator_double(self):
        rules = [{
                "id" : "6b1c4ede475775aa",
                "input_type" : "Double",
                "name" : "Double",
                "full_name" : "Double",
                "range" : [0, 1.79769e+308]
                }]
        validator = Validator(rules)

        self.assertEqual(validator.validate(0).valid, True)
        self.assertEqual(validator.validate(3.14).valid, True)
        self.assertEqual(validator.validate(1.79769e+308).valid, True)

        result = validator.validate(1.7977e+308)
        self.assertEqual(result.valid, False)
        self.assertIsInstance(result.messages[0]['exception'], ValueTooBig)

        result = validator.validate(-0.1e-30)
        self.assertEqual(result.valid, False)
        self.assertIsInstance(result.messages[0]['exception'], ValueTooSmall)

        result = validator.validate('asd')
        self.assertEqual(result.valid, False)
        self.assertIsInstance(result.messages[0]['exception'], ValidationTypeError)

    def test_validator_bool(self):
        rules = [{
                "id" : "282546d52edd4",
                "input_type" : "Bool",
                "name" : "Bool",
                "full_name" : "Bool"
                }]
        validator = Validator(rules)

        self.assertEqual(validator.validate(True).valid, True)
        self.assertEqual(validator.validate(False).valid, True)

        result = validator.validate(0)
        self.assertEqual(result.valid, False)
        self.assertIsInstance(result.messages[0]['exception'], ValidationTypeError)

    def test_validator_string(self):
        rules = [{
                "id" : "29b5533100b6f60f",
                "input_type" : "String",
                "name" : "String",
                "full_name" : "String"
                }]
        validator = Validator(rules)
        
        self.assertEqual(validator.validate("sdfadsf sdaf").valid, True)

        result = validator.validate(23)
        self.assertEqual(result.valid, False)
        self.assertIsInstance(result.messages[0]['exception'], ValidationTypeError)

    def test_validator_filename(self):
        rules = [{
                "id" : "89a808b8e9515bf8",
                "name" : "FileName_input",
                "full_name" : "FileName_input",
                "input_type" : "FileName",
                "file_mode" : "input"
                }]
        validator = Validator(rules)
        

        self.assertEqual(validator.validate("sdfadsf sdaf").valid, True)
        self.assertEqual(validator.validate(r"C:\flow.ini").valid, True)
        self.assertEqual(validator.validate(r"/home/user/flow.ini").valid, True)

        result = validator.validate(23)
        self.assertEqual(result.valid, False)
        self.assertIsInstance(result.messages[0]['exception'], ValidationTypeError)

    def test_validator_selection(self):
        rules = [{
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
                }]
        validator = Validator(rules)

        self.assertEqual(validator.validate('PETSc').valid, True)
        self.assertEqual(validator.validate('petsc').valid, True)

        result = validator.validate('asd')
        self.assertEqual(result.valid, False)
        self.assertIsInstance(result.messages[0]['exception'], InvalidOption)

    def test_validator_array(self):
        rules = [{
                "id" : "eee3033466b9ffa2",
                "input_type" : "Array",
                "range" : [0, 4294967295],
                "subtype" : "6b1c4ede475775aa"
                }, {
                "id" : "6b1c4ede475775aa",
                "input_type" : "Double",
                "name" : "Double",
                "full_name" : "Double",
                "range" : [0, 10.5]
                }]
        validator = Validator(rules)

        self.assertEqual(validator.validate([]).valid, True)
        self.assertEqual(validator.validate([0, 1.5]).valid, True)
        self.assertEqual(validator.validate([0, 3.2, 3, 8.4]).valid, True)

        result = validator.validate([-1 0 'a' 3.3 10.6])
        self.assertIsInstance(result.messages[0]['exception'], ValueTooSmall)
        self.assertIsInstance(result.messages[1]['exception'], ValidationTypeError)
        self.assertIsInstance(result.messages[2]['exception'], ValueTooBig)

    def test_validator_array_length(self):
        rules = [{
                "id" : "eee3033466b9ffa2",
                "input_type" : "Array",
                "range" : [2, 2],
                "subtype" : "6b1c4ede475775aa"
                }, {
                "id" : "6b1c4ede475775aa",
                "input_type" : "Double",
                "name" : "Double",
                "full_name" : "Double",
                "range" : [0, 1.79769e+308]
                }]
        validator = Validator(rules)

        self.assertEqual(validator.validate([0, 43.2]).valid, True)

        result = validator.validate([1])
        self.assertEqual(result.valid, False)
        self.assertIsInstance(result.messages[0]['exception'], NotEnoughItems)

        result = validator.validate([1 2 3])
        self.assertEqual(result.valid, False)
        self.assertIsInstance(result.messages[0]['exception'], TooManyItems)


class TestValidationResult(unittest.TestCase):

    def test_report(self):
        result = ValidationResult()
        self.assertEqual(result.valid, True)

        result.report({'severity': Severity.debug})
        self.assertEqual(result.valid, True)

        result.report({'severity': Severity.info})
        self.assertEqual(result.valid, True)

        result.report({'severity': Severity.warn})
        self.assertEqual(result.valid, True)

        result.report({'severity': Severity.error})
        self.assertEqual(result.valid, False)

