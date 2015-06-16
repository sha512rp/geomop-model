# -*- coding: utf-8 -*-
"""
Validator for Flow123D CON files

@author: Tomas Krizek
"""

from .errors import *
from . import checks


class Validator:
    SCALAR = ['Integer', 'Double', 'Bool', 'String', 'Selection', 'FileName']

    @property
    def errors(self):
        return tuple(self._errors)

    @property
    def console_log(self):
        out = ('VALID' if self.valid else 'INVALID')
        for node, error in self._errors:
            out = out + '\n' + node.path + ': ' + str(error)
        return out

    def validate(self, node, its=None):
        """
        Performs data validation of node.

        Validation is performed recursively on all children nodes as well.

        Returns True when all data was correctly validated, False otherwise.
        Attribute errors contains a list of occured errors.
        """
        self._errors = []
        self.valid = True

        if its is None:
            its = node.its

        self._validate_node(node, its)
        self._errors = reversed(self._errors)

        return self.valid

    def _validate_node(self, node, its=None):
        """
        Determines if node contains correct value.

        Method verifies node recursively. All descendant nodes are checked.
        """
        if its is None:
            its = node.its
        
        if its.input_type in Validator.SCALAR:
            self._validate_scalar(node, its)
        elif its.input_type == 'Record':
            self._validate_record(node, its)
        elif its.input_type == 'AbstractRecord':
            self._validate_abstract(node, its)
        elif its.input_type == 'Array':
            self._validate_array(node, its)
        else:
            raise Exception("Format error: Unknown input_type '"
                + its.input_type + "'")

    def _validate_scalar(self, node, its):
        try:
            getattr(checks, 'check_%s' % its.input_type.lower())(node.value, its)
        except ValidationError as error:
            self._report_error(node, error)

    def _validate_record(self, node, its):
        if not isinstance(node.value, dict):
            self._report_error(node, ValidationError("Expecting type Record"))
            return
        for key in its.keys.keys():
            try:
                checks.check_record_key(node.value, key, its)
            except ValidationError as error:
                self._report_error(node, error)
                if isinstance(error, UnknownKey):
                    continue
            if key in node.value:
                self._validate_node(node.value[key], its.keys[key]['type'])

    def _validate_abstract(self, node, its):
        try:
            record_its = checks.get_abstractrecord_type(node.value, its)
        except ValidationError as error:
            self._report_error(node, error)
        else:
            self._validate_record(node, record_its)

    def _validate_array(self, node, its):
        if not isinstance(node.value, list):
            self._report_error(node, ValidationError("Expecting type Array"))
            return
        try:
            checks.check_array(node.value, its)
        except ValidationError as error:
            self._report_error(node, error)
        for item in node.value:
            self._validate_node(item, its.subtype)

    def __init__(self):
        self.valid = True
        self._errors = []

    def _report_error(self, node, error):
        """
        Report an error.
        """
        self.valid = False
        self._errors.append((node, error))


