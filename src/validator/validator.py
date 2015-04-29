# -*- coding: utf-8 -*-
"""
Validator for Flow123D CON files

@author: Tomas Krizek
"""

from enum import Enum

from geomopcontext.validator.errors import *
import geomopcontext.validator.rules as rules


SCALARS = ['Integer', 'Double', 'Bool', 'String', 'Selection',
                    'FileName']


def validate(node, format):
    """
    Performs data validation from the root rule.

    Returns True if valid, list of errors otherwise.
    """
    pass


def validate_node(node):
    try:
        return getattr(rules,
            'check_%s' % node.its.input_type.lower())(node.value, node.its)
    except ValidationError as e:
        raise ValidationError(node.path + ': ' + str(e))


def _validate_scalar(data, its):
    # try:
    #     getattr(rules, 'check_%s' % its.input_type.lower())(data,
    #         **rule.kwargs)
    # except ValidationError as e:
    #     self.result.report({'severity': Severity.error,\
    #                         'message': str(e),\
    #                         'exception': e})
    #     # TODO position of exception
    pass


def _validate_array(data, rule):
    pass


# def _validate_record(self, data, )


class Severity(Enum):
    debug = 1
    info = 2
    warn = 3
    error = 4


class ValidationResult:

    def __init__(self):
        self.messages = []
        self.valid = True

    def report(self, message):
        """
        Register a new message.

        If message severity exceeds error level, valid is set to False.
        """
        if message['severity'].value >= Severity.error.value:
            self.valid = False
        self.messages.append(message)

    def get_all(self, minimum_severity=Severity.warn):
        """
        Returns all messages of minimum_severity and above.

        minimum_severity: default Severity.warn 
        """
        out = []
        for message in self.messages:
            if message['severity'].value >= minimum_severity.value:
                out.append(message)
        return out
