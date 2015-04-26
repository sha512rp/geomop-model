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

    def its(self, key=None):
        """
        Return ITS for given id or type_name.

        If key is not specified, returns root ITS.
        """
        if key is None:
            key = self.root_id  # use root if no key is specified
        try:  # assume id
            return self.types[key]
        except KeyError:
            try:  # assume type_name
                return self.named_types[key]
            except KeyError:
                return None


class InputTypeSpec:
    OPTIONAL_PARAMS = ['name', 'full_name', 'description']

    def __init__(self, data):
        self.id = data['id']
        self.input_type = data['input_type']
        for param in InputTypeSpec.OPTIONAL_PARAMS:
            self.__parse_optional(data, param)
        try:        # parse extra parameters based on input_type
            getattr(self, '_parse_%s' % self.input_type.lower())(data)
        except AttributeError:
            pass

    def __parse_range(self, data, default=[float('-inf'), float('inf')]):
        try:
            self.min = data['range'][0]
        except KeyError:
            self.min = default[0]

        try:
            self.max = data['range'][1]
        except KeyError:
            self.max = default[1]

    def __parse_optional(self, data, key):
        try:
            setattr(self, key, data[key])
        except KeyError:
            pass

    def _parse_integer(self, data):
        self.__parse_range(data)

    def _parse_double(self, data):
        self.__parse_range(data)

    def _parse_selection(self, data):
        self.values = KeySet(data['values'], key_label='name')

    def _parse_filename(self, data):
        self.file_mode = data['file_mode']

    def _parse_array(self, data):
        self.__parse_range(data, default=[0, float('inf')])
        self.subtype = data['subtype']

    def _parse_record(self, data):
        self.type_name = data['type_name']
        self.keys = KeySet(data['keys'])

        for key in ['type_full_name', 'implements']:
            self.__parse_optional(data, key)

    def _parse_abstractrecord(self, data):
        self.implementations = data['implementations']

        self.__parse_optional(data, 'default_descendant')


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

