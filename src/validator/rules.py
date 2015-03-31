# -*- coding: utf-8 -*-
"""
Basic rules for data validation

@author: Tomas Krizek
"""

from errors import *


def check_integer(val, min=float("-inf"), max=float("inf")):
    if not isinstance(val, int):
        raise TypeError("Expecting 'int' type")

    if (val < min):
        raise ValueTooSmall(min)

    if (val > max):
        raise ValueTooBig(max)

    return True


def check_double(val, min=float("-inf"), max=float("inf")):
    if not isinstance(val, (int, float)):
        raise TypeError("Expecting 'float' type")

    if (val < min):
        raise ValueTooSmall(min)

    if (val > max):
        raise ValueTooBig(max)
    # except 

    return True

