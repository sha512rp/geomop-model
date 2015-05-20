# -*- coding: utf-8 -*-
"""
GeoMop Model

Errors of data validation

@author: Tomas Krizek
"""


class ValidationError(Exception):
    pass


class ValidationTypeError(ValidationError):
    pass


class ValueTooSmall(ValidationError):
    def __init__(self, expected):
        message = "Expected value larger or equal to " + str(expected)
        super(ValueTooSmall, self).__init__(message)


class ValueTooBig(ValidationError):
    def __init__(self, expected):
        message = "Expected value smaller or equal to " + str(expected)
        super(ValueTooBig, self).__init__(message)


class InvalidOption(ValidationError):
    def __init__(self, option, selection_name):
        message = "Option '" + option + "' does not exist in selection " + \
                selection_name
        super(InvalidOption, self).__init__(message)


class NotEnoughItems(ValidationError):
    def __init__(self, expected):
        message = "Expected at least " + str(expected) + " items"
        super(NotEnoughItems, self).__init__(message)


class TooManyItems(ValidationError):
    def __init__(self, expected):
        message = "Expected at most " + str(expected) + " items"
        super(TooManyItems, self).__init__(message)


class UnknownKey(ValidationError):
    def __init__(self, key, record_name):
        message = "Unknown key '" + key + "' in record " + \
                record_name
        super(UnknownKey, self).__init__(message)


class MissingKey(ValidationError):
    def __init__(self, key, record_name):
        message = "Missing obligatory key '" + key + "' in record " + \
                record_name
        super(MissingKey, self).__init__(message)


class MissingAbstractRecordType(ValidationError):
    def __init__(self):
        message = "Missing abstract record type"
        super(MissingAbstractRecordType, self).__init__(message)


class InvalidAbstractRecordType(ValidationError):
    def __init__(self, type_name, abstract_name):
        message = "Invalid TYPE '" + type_name + "' for " + abstract_name
        super(InvalidAbstractRecordType, self).__init__(message)



