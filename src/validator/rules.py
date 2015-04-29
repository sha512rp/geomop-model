# -*- coding: utf-8 -*-
"""
Basic rules for data validation

@author: Tomas Krizek
"""

from geomopcontext.validator.errors import *


def check_integer(val, its):
    if not isinstance(val, int):
        raise ValidationTypeError("Expecting type Integer")

    if (val < its.min):
        raise ValueTooSmall(its.min)

    if (val > its.max):
        raise ValueTooBig(its.max)

    return True


def check_double(val, its):
    if not isinstance(val, (int, float)):
        raise ValidationTypeError("Expecting type Double")

    if (val < its.min):
        raise ValueTooSmall(its.min)

    if (val > its.max):
        raise ValueTooBig(its.max)

    return True


def check_bool(val, its):
    if not isinstance(val, bool):
        raise ValidationTypeError("Expecting type Bool")

    return True


def check_string(val, its):
    if not isinstance(val, str):
        raise ValidationTypeError("Expecting type String")

    return True


def check_selection(val, its):
    if (val in its.values.keys()):
        return True
    else:
        raise InvalidOption(val, its.name)


def check_filename(val, its):
    """
    Placeholder for FileName validation.
    """
    return check_string(val, its)


def check_array(val, its):
    if not isinstance(val, (list, str)):
        raise ValidationTypeError("Expecting type Array")

    if len(val) < its.min:
        raise NotEnoughItems(its.min)
    elif len(val) > its.max:
        raise TooManyItems(its.max)

    return True
