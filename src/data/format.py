# -*- coding: utf-8 -*-
"""
Contains format specification class and methods to parse it from JSON.

@author: Tomas Krizek
"""

import copy
from collections import namedtuple


class FormatSpec:
    """
    Contains complete input type specification (ITS).

    Functions:
        - return default value for any path
    """

    def __init__(self, data):
        """Initialize the class by parsing ITS from JSON data."""
        self.types = {}
        self.named_types = {}
        self.root_id = data[0]['id']      # set root type
        for item in data:
            its = InputTypeSpec(item)
            self.types[its.id] = its  # register by id
            try:  # register by type_name
                type_name = its.type_name
            except AttributeError:
                pass  # not specified type_name -> skip
            else:
                self.named_types[type_name] = its


    def get_its(self, key=None):
        """
        Return ITS for given id, type_name or path.

        id: randomly assigned hex number (from JSON data)
        path: points to any node in the tree, starts with /
        """
        if key is None:
            key = self.root_id  # use root if no key is specified
        try:  # assume id
            return self.types[key]
        except KeyError:
            try:  # assume type_name
                return self.named_types[key]
            except KeyError:
                # try to interpet key as path
                # TODO implement
                return None



class InputTypeSpec:
    OPTIONAL_PARAMS = ['name', 'full_name', 'description']

    def __init__(self, data):
        self.id = data['id']
        self.input_type = data['input_type']
        for param in InputTypeSpec.OPTIONAL_PARAMS:       # parse optional parameters
            try:
                setattr(self, param, data[param])
            except KeyError:
                pass
        try:        # parse extra parameters based on input_type
            getattr(self, '_parse_%s' % self.input_type.lower())(data)
        except AttributeError:
            self.kwargs = {}

    def _parse_integer(self, data):
        self.min = data['range'][0]
        self.max = data['range'][1]

    def _parse_double(self, data):
        self.min = data['range'][0]
        self.max = data['range'][1]

    def _parse_selection(self, data):
        self.values = KeySet(data['values'], key_label='name')

    def _parse_filename(self, data):
        self.file_mode = data['file_mode']

    def _parse_array(self, data):
        self.min = data['range'][0]
        self.max = data['range'][1]
        self.subtype = data['subtype']

    def _parse_record(self, data):
        self.type_name = data['type_name']
        self.keys = KeySet(data['keys'])

        try:  # optional
            self.type_full_name = data['type_full_name']
        except KeyError:
            pass

        try:  # optional
            self.implements = data['implements']
        except KeyError:
            pass

    def _parse_abstractrecord(self, data):
        self.implementations = data['implementations']

        try:  # optional
            self.default_descendant = data['default_descendant']
        except KeyError:
            pass


class KeySet:
    """
    KeySet is constructed from list of dicts.

    Supports:
      - dot notation: returns value for keyset.key.subkey
      - iteration: returns values of all possible keys (top level)
      - length: returns number of keys (top level)
      - contains: key in keyset
    """

    def __init__(self, data, key_label='key'):
        """
            key_label: this identifier will be used as a key
        """
        for item in data:
            value = ObjectView(item)
            self.__dict__[item[key_label]] = value

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        for name in self.__dict__.keys():
            yield self.__dict__[name]

    def __contains__(self, item):
        return item in self.__dict__.keys()


class ObjectView:
    """
    ObjectView transforms dict into object with dot notation.
    Supports nested dicts.
    No reference to original dict.
    """
    def __init__(self, d):
        self.__dict__ = copy.deepcopy(d)
        for key, value in self.__dict__.items():
            if isinstance(value, dict):
                self.__dict__[key] = ObjectView(value)

