# -*- coding: utf-8 -*-
"""
Errors of data validation

@author: Tomas Krizek
"""


class ValueTooSmall(Exception):
    def __init__(self, expected):

        message = "Expected value larger or equal to " + str(expected) + ""

        # Call the base class constructor with the parameters it needs
        super(ValueTooSmall, self).__init__(message)


class ValueTooBig(Exception):
    def __init__(self, expected):

        message = "Expected value smaller or equal to " + str(expected) + ""

        # Call the base class constructor with the parameters it needs
        super(ValueTooBig, self).__init__(message)
