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
    elif its.input_type == 'Record':
        return _validate_record(node, its)
    elif its.input_type == 'AbstractRecord':
        return _validate_abstract(node, its)
    else:
        raise Exception("Format error: Unknown input_type '"
            + its.input_type + "'")

def _validate_simple_check(node, its):
    result = ValidationResult()
    try:
        getattr(rules, 'check_%s' % its.input_type.lower())(node.value, its)
    except ValidationError as error:
        _report_validation_error(result, error, node)
    return result


def _validate_record(node, its):
    result = ValidationResult()
    keys = list(node.value.keys()) + list(its.keys.keys())
    for key in keys:
        try:
            rules.check_record_key(node.value, key, its)
        except ValidationError as error:
            _report_validation_error(result, error, node)
    return result


def _validate_abstract(node, its):
    try:
        record_its = rules.get_abstractrecord_type(node.value, its)
    except ValidationError as error:
        result = ValidationResult()
        _report_validation_error(result, error, node)
        return result
    else:
        return _validate_record(node, record_its)


def _report_validation_error(result, error, node):
    result.report(ValidationError(node.path + ': ' + str(error)))