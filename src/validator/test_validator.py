# -*- coding: utf-8 -*-
"""
Tests for validator

@author: Tomas Krizek
"""

import unittest
from geomopcontext.validator.validator import Validator

class TestBasicRules(unittest.TestCase):

    def setUp(self):
        # rules = 

        # validator = Validator()
        # validator.parse_rules()
        pass

    def test_validator_selection(self):
        rule = {
                "id" : "f9756fb2f66076a1",
                "input_type" : "Selection",
                "name" : "PartTool",
                "full_name" : "PartTool",
                "description" : "Select the partitioning tool to use.",
                "values" : [
                { "value" : "0",
                 "name" : "PETSc",
                "description" : "Use PETSc interface to various partitioning tools." },
                { "value" : "1",
                 "name" : "METIS",
                "description" : "Use direct interface to Metis." }]
                }
        pass
