# -*- coding: utf-8 -*-
"""
Basic rules for data validation

@author: Tomas Krizek
"""

from geomopcontext.validator.errors import *


def check_integer(value, its):
    if not isinstance(value, int):
        raise ValidationTypeError("Expecting type Integer")

    if (value < its.min):
        raise ValueTooSmall(its.min)

    if (value > its.max):
        raise ValueTooBig(its.max)

    return True


def check_double(value, its):
    if not isinstance(value, (int, float)):
        raise ValidationTypeError("Expecting type Double")

    if (value < its.min):
        raise ValueTooSmall(its.min)

    if (value > its.max):
        raise ValueTooBig(its.max)

    return True


def check_bool(value, its):
    if not isinstance(value, bool):
        raise ValidationTypeError("Expecting type Bool")

    return True


def check_string(value, its):
    if not isinstance(value, str):
        raise ValidationTypeError("Expecting type String")

    return True


def check_selection(value, its):
    if (value in its.values):
        return True
    else:
        raise InvalidOption(value, its.name)


def check_filename(value, its):
    """
    Placeholder for FileName validation.
    """
    return check_string(value, its)


def check_array(value, its):
    if not isinstance(value, (list, str)):
        raise ValidationTypeError("Expecting type Array")

    if len(value) < its.min:
        raise NotEnoughItems(its.min)
    elif len(value) > its.max:
        raise TooManyItems(its.max)

    return True


def check_record_key(record, key, its):
    if not isinstance(record, dict):
        raise ValidationTypeError("Expecting type Record")

    if key not in its.keys and key != 'TYPE':
        raise UnknownKey(key, its.name)

    try:
        key_type = its.keys[key]['default']['type']
    except KeyError:
        pass  # if default or type isn't specified, skip
    else:
        if key_type == 'obligatory':
            try:
                record[key]
            except KeyError:
                raise MissingKey(key, its.name)

    return True


def get_abstractrecord_type(record, its):
    if not isinstance(record, dict):
        raise ValidationTypeError("Expecting type (Abstract)Record")

    try:
        type_name = record['TYPE']
    except KeyError:
        try:
            type_ = its.default_descendant
        except AttributeError:
            raise MissingAbstractRecordType()
    else:
        try:
            type_ = its.implementations[type_name]
        except KeyError:
            raise InvalidAbstractRecordType(type_name, its.name)

    return type_

