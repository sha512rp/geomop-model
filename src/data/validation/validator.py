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
        for path, error in sorted(self._errors, key=(lambda item: item[0])):
            out = out + '\n' + path + ': ' + str(error)
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
        self.root_node = node

        if its is None:
            its = node.its

        self._validate_node('', its)
        self._errors = reversed(self._errors)

        return self.valid

    def _validate_node(self, path='', its=None):
        """
        Determines if node at given path contains correct value.

        Method verifies node recursively. All descendant nodes are checked.
        """
        node = self.root_node.get(path)
        if its is None:
            its = node.its
        
        if its.input_type in Validator.SCALAR:
            self._validate_scalar(path, its)
        elif its.input_type == 'Record':
            self._validate_record(path, its)
        elif its.input_type == 'AbstractRecord':
            self._validate_abstract(path, its)
        elif its.input_type == 'Array':
            self._validate_array(path, its)
        else:
            raise Exception("Format error: Unknown input_type '"
                + its.input_type + "'")

    def _validate_scalar(self, path, its):
        node = self.root_node.get(path)
        try:
            getattr(checks, 'check_%s' % its.input_type.lower())(node.value, its)
        except ValidationError as error:
            self._report_error(path, error)

    def _validate_record(self, path, its):
        node = self.root_node.get(path)
        if not isinstance(node.value, dict):
            self._report_error(path, ValidationError("Expecting type Record"))
            return
        for key in its.keys.keys():
            try:
                checks.check_record_key(node.value, key, its)
            except ValidationError as error:
                self._report_error(path, error)
                if isinstance(error, UnknownKey):
                    continue
            if key in node.value:
                self._validate_node('%s/%s' % (path, key), its.keys[key]['type'])

    def _validate_abstract(self, path, its):
        node = self.root_node.get(path)
        try:
            record_its = checks.get_abstractrecord_type(node.value, its)
        except ValidationError as error:
            self._report_error(path, error)
        else:
            self._validate_record(path, record_its)

    def _validate_array(self, path, its):
        node = self.root_node.get(path)
        if not isinstance(node.value, list):
            self._report_error(path, ValidationError("Expecting type Array"))
            return
        try:
            checks.check_array(node.value, its)
        except ValidationError as error:
            self._report_error(path, error)
        for i, item in enumerate(node.value):
            self._validate_node('%s/%d' % (path, i), its.subtype)

    def __init__(self):
        self.valid = True
        self._errors = []

    def _report_error(self, path, error):
        """
        Report an error.
        """
        self.valid = False
        self._errors.append((path, error))


