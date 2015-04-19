# -*- coding: utf-8 -*-
"""
Basic rules for data validation

@author: Tomas Krizek
"""

from geomopcontext.validator.errors import *
from geomopcontext.data.selection import Selection


class Rule:
    OPTIONAL_PARAMS = ['name', 'full_name', 'description']

    def __init__(self, data):
        self.id = data['id']
        self.input_type = data['input_type']
        for param in Rule.OPTIONAL_PARAMS:       # parse optional parameters
            try:
                setattr(self, param, data[param])
            except KeyError:
                pass
        try:        # parse extra parameters based on input_type
            print('_parse_%s' % self.input_type.lower())
            getattr(self, '_parse_%s' % self.input_type.lower())(data)
        except AttributeError:
            self.kwargs = {}

    def _parse_integer(self, data):
        self.kwargs = {'min': data['range'][0],\
                     'max': data['range'][1]}

    def _parse_double(self, data):
        self.kwargs = {'min': data['range'][0],\
                     'max': data['range'][1]}

    def _parse_selection(self, data):
        self.selection = Selection(self.name, data['values'])
        self.kwargs = {'selection': self.selection}

    def _parse_filename(self, data):
        self.kwargs = {'file_mode': data['file_mode']}

    def _parse_array(self, data):
        self.kwargs = {'min': data['range'][0],\
                     'max': data['range'][1]}

     # TODO implement _parse_record, _parse_abstract_record



def check_integer(val, min=float("-inf"), max=float("inf")):
    if not isinstance(val, int):
        raise ValidationTypeError("Expecting type Integer")

    if (val < min):
        raise ValueTooSmall(min)

    if (val > max):
        raise ValueTooBig(max)

    return True


def check_double(val, min=float("-inf"), max=float("inf")):
    if not isinstance(val, (int, float)):
        raise ValidationTypeError("Expecting type Double")

    if (val < min):
        raise ValueTooSmall(min)

    if (val > max):
        raise ValueTooBig(max)

    return True


def check_bool(val):
    if not isinstance(val, bool):
        raise ValidationTypeError("Expecting type Bool")

    return True


def check_string(val):
    if not isinstance(val, str):
        raise ValidationTypeError("Expecting type String")

    return True


def check_selection(val, selection=None):
    if (selection.has(val)):
        return True
    else:
        raise InvalidOption(selection)


def check_filename(val, file_mode=None):
    """
    Placeholder for FileName validation.
    """
    return check_string(val)
