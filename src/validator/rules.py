# -*- coding: utf-8 -*-
"""
Basic rules for data validation

@author: Tomas Krizek
"""

from geomopcontext.validator.errors import *


# class RuleParser:
#     def __init__(self):
#         self.rules = {}

#     def parse(self, rules):
#         """
#         Parse Flow123D JSON objects representing documentation
#         and extract rule sets.
#         """
#         for rule in rules:



class Rule:
    def __init__(self, id, name, full_name):
        self.id = id
        self.name = name
        self.full_name = full_name



def check_integer(val, min=float("-inf"), max=float("inf")):
    if not isinstance(val, int):
        raise TypeError("Expecting type Integer")

    if (val < min):
        raise ValueTooSmall(min)

    if (val > max):
        raise ValueTooBig(max)

    return True


def check_double(val, min=float("-inf"), max=float("inf")):
    if not isinstance(val, (int, float)):
        raise TypeError("Expecting type Double")

    if (val < min):
        raise ValueTooSmall(min)

    if (val > max):
        raise ValueTooBig(max)

    return True


def check_bool(val):
    if not isinstance(val, bool):
        raise TypeError("Expecting type Bool")

    return True


def check_string(val):
    if not isinstance(val, str):
        raise TypeError("Expecting type String")

    return True


def check_selection(selection, value):
    if (selection.has(value)):
        return True
    else:
        raise InvalidOption(selection)


