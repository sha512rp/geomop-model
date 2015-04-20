# -*- coding: utf-8 -*-
"""
Errors of data validation

@author: Tomas Krizek
"""


class ValidationError(Exception):
    pass


class ValidationTypeError(ValidationError):
    pass


class ValueTooSmall(ValidationError):
    def __init__(self, expected):
        message = "Expected value larger or equal to " + str(expected) + ""

        super(ValueTooSmall, self).__init__(message)


class ValueTooBig(ValidationError):
    def __init__(self, expected):
        message = "Expected value smaller or equal to " + str(expected) + ""

        super(ValueTooBig, self).__init__(message)


class InvalidOption(ValidationError):
    def __init__(self, selection):
        message = "Invalid option for selection " + \
                str(selection.name) + ""

        super(InvalidOption, self).__init__(message)


class NotEnoughItems(ValidationError):
    def __init__(self, expected):
        message = "Expected at least " + str(expected) + " items"

        super(ValueTooBig, self).__init__(message)


class TooManyItems(ValidationError):
    def __init__(self, expected):
        message = "Expected at most " + str(expected) + " items"

        super(ValueTooBig, self).__init__(message)

