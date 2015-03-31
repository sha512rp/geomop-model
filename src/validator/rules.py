# -*- coding: utf-8 -*-
"""
Basic rules for data validation

@author: Tomas Krizek
"""

from errors import *


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
