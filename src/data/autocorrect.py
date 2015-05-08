# -*- coding: utf-8 -*-
"""
Auto-correct module for GeomMop Model data

@author: Tomas Krizek
"""

from copy import copy

from geomopcontext.data.con import DataNode


def expand(node, its=None):
    """
    Performs recursive auto-correction.

    Auto-correction:
        1. If Array is expected and scalar/record is found, encapsulate it
           in Array(s).
        2. If Record is expected and scalar/array is found, check
           reducible_to_key. If present, create the Record.
        3. If AbstractRecord is expected and scalar/array is found, check if
           default_descendant fits rule 2.
    """
    pass


def _get_expected_array_dimension(its):
    dim = 0
    while its.input_type == 'Array':
        dim = dim + 1
        its = its.subtype
    return dim


def _expand_value_to_array(node, dim):
    """Expands node value to specified dimension."""
    value = node.value
    while dim > 0:
        value = [value]
        dim = dim - 1
    return DataNode(value, node.parent, node.name)


def _expand_reducible_to_key(node, its):
    try:
        key = its.default_descendant.reducible_to_key
    except AttributeError:
        key = its.reducible_to_key

    value = {}
    value[key] = node
    return DataNode(value, node.parent, node.name)


def _is_reducible_to_key(node, its):
    try:  # is Record reducible to key?
        its.reducible_to_key
    except AttributeError:
        try:
            its.default_descendant.reducible_to_key
        except AttributeError:
            return False
        else:
            return True
    else:
        return True
