# -*- coding: utf-8 -*-
"""
Validator for Flow123D CON files

@author: Tomas Krizek
"""

from enum import Enum

from geomopcontext.validator.errors import *
import geomopcontext.validator.rules as rules
from geomopcontext.validator.rules import Rule

class Validator:

    SCALARS = ['Integer', 'Double', 'Bool', 'String', 'Selection',
                    'FileName']

    def __init__(self, json_rules):
        self.rules = {}
        self.root_id = json_rules[0]['id']      # set root validation rule
        for rule in json_rules:
            self.rules[rule['id']] = Rule(rule)

    def validate(self, data):
        """
        Performs data validation from the root rule.

        Returns True if valid, list of errors otherwise.
        """
        self.result = ValidationResult()
        if not self.rules:
            self.result.report({'severity': Severity.warn,
                'message': "No rules were specified"})
        self._validate(data, self.root_id)
        return self.result

    def _validate(self, data, rule_id):
        rule = self.rules[rule_id]
        if rule.input_type in Validator.SCALARS:
            self._validate_scalar(data, rule)
        elif rule.input_type == 'Record':
            self._validate_record(data, rule)
        elif rule.input_type == 'AbstractRecord':
            self._validate_abstract_record(data, rule)
        else:
            self.result.report({'severity': Severity.warn, 'message': 
                "Unknown rule input_type: " + rule.input_type})

    def _validate_scalar(self, data, rule):
        try:
            getattr(rules, 'check_%s' % rule.input_type.lower())(data,
                **rule.kwargs)
        except ValidationError as e:
            self.result.report({'severity': Severity.error,\
                                'message': str(e),\
                                'exception': e})
            # TODO position of exception


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
            if message['severity'].value >= minimum_severity:
                out.append(message)
        return out
