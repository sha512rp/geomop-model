# -*- coding: utf-8 -*-
"""
Tests for validator

@author: Tomas Krizek
"""

import unittest

from geomopcontext.validator.validator import Validator, ValidationResult, Severity
from geomopcontext.validator.errors import *

class TestValidator(unittest.TestCase):

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
        self.assertIsInstance(result.messages[0]['exception'], InvalidOption)
        self.assertEqual(result.valid, False)


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

