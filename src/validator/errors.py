# -*- coding: utf-8 -*-
"""
Errors of data validation

@author: Tomas Krizek
"""


class ValueTooSmall(Exception):
    def __init__(self, expected):
        message = "Expected value larger or equal to " + str(expected) + ""

        super(ValueTooSmall, self).__init__(message)


class ValueTooBig(Exception):
    def __init__(self, expected):
        message = "Expected value smaller or equal to " + str(expected) + ""

        super(ValueTooBig, self).__init__(message)


class InvalidOption(Exception):
    def __init__(self, selection):
        message = "Invalid option for selection " + \
                str(selection.name) + ""

        super(InvalidOption, self).__init__(message)