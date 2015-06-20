# -*- coding: utf-8 -*-
"""
Basic rules for data validation

@author: Tomas Krizek
"""

from . import errors


def check_integer(value, its):
    if not isinstance(value, int):
        raise errors.ValidationTypeError("Expecting type Integer")

    if (value < its.min):
        raise errors.ValueTooSmall(its.min)

    if (value > its.max):
        raise errors.ValueTooBig(its.max)

    return True


def check_double(value, its):
    if not isinstance(value, (int, float)):
        raise errors.ValidationTypeError("Expecting type Double")

    if (value < its.min):
        raise errors.ValueTooSmall(its.min)

    if (value > its.max):
        raise errors.ValueTooBig(its.max)

    return True


def check_bool(value, its):
    if not isinstance(value, bool):
        raise errors.ValidationTypeError("Expecting type Bool")

    return True


def check_string(value, its):
    if not isinstance(value, str):
        raise errors.ValidationTypeError("Expecting type String")

    return True


def check_selection(value, its):
    if (value in its.values):
        return True
    else:
        raise errors.InvalidOption(value, its.name)


def check_filename(value, its):
    """
    Placeholder for FileName validation.
    """
    return check_string(value, its)


def check_array(value, its):
    if not isinstance(value, (list, str)):
        raise errors.ValidationTypeError("Expecting type Array")

    if len(value) < its.min:
        raise errors.NotEnoughItems(its.min)
    elif len(value) > its.max:
        raise errors.TooManyItems(its.max)

    return True


def check_record_key(record, key, its):
    if not isinstance(record, dict):
        raise errors.ValidationTypeError("Expecting type Record")

    # if key is not found in specifications, it is considered to be valid
    if key not in its.keys and key != 'TYPE':
        # raise UnknownKey(key, its.type_name)
        return True

    try:
        key_type = its.keys[key]['default']['type']
    except KeyError:
        pass  # if default or type isn't specified, skip
    else:
        if key_type == 'obligatory':
            try:
                record[key]
            except KeyError:
                raise errors.MissingKey(key, its.type_name)

    return True


def get_abstractrecord_type(record, its):
    try:
        type_name = record['TYPE'].value
    except (KeyError, TypeError):
        try:
            type_ = its.default_descendant
        except AttributeError:
            raise errors.MissingAbstractRecordType()
    else:
        try:
            type_ = its.implementations[type_name]
        except KeyError:
            raise errors.InvalidAbstractRecordType(type_name, its.name)

    return type_

