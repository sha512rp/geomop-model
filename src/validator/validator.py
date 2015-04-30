# -*- coding: utf-8 -*-
"""
Validator for Flow123D CON files

@author: Tomas Krizek
"""

from enum import Enum

from geomopcontext.validator.errors import *
import geomopcontext.validator.rules as rules


SIMPLE_CHECKS = ['Integer', 'Double', 'Bool', 'String',
                    'Selection', 'FileName', 'Array']


def validate(node, format):
    """
    Performs data validation from the root rule.

    Returns True if valid, list of errors otherwise.
    """
    pass


def validate_node(node, its=None):
    if its is None:
        its = node.its
    
    if its.input_type in SIMPLE_CHECKS:
        return _validate_simple_check(node, its)


def _validate_simple_check(node, its):
    result = ValidationResult()
    try:
        getattr(rules, 'check_%s' % its.input_type.lower())(node.value, its)
    except ValidationError as error:
        _report_validation_error(result, error, node)
    return result


def _report_validation_error(result, error, node):
    result.report(type(error)(node.path + ': ' + str(error)))


class ValidationResult:

    def __init__(self):
        self._errors = []
        self.valid = True

    def report(self, error):
        """
        Report an error.
        """
        self.valid = False
        self._errors.append(error)

    @property
    def errors(self):
        return tuple(self._errors)
