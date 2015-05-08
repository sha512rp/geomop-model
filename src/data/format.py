# -*- coding: utf-8 -*-
"""
Contains format specification class and methods to parse it from JSON.

@author: Tomas Krizek
"""

import json


def parse_format(filename):
    """Return root ITS."""
    return FormatSpec(json.load(open(filename))).its()


class FormatSpec:
    """
    Contains complete input type specification (ITS).
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
        self._substitute_ids_with_references()

    def _substitute_ids_with_references(self):
        """
        Creates links between ITS. Replaces ids with references.
        """
        for key, its in self.types.items():
            if its.input_type == 'Array':
                its.subtype = self.types[its.subtype]
            elif its.input_type == 'AbstractRecord':
                self._substitute_implementations(its)
                self._substitute_default_descendant(its)
            elif its.input_type == 'Record':
                self._substitute_key_type(its)

    def _substitute_implementations(self, its):
        impls = {}
        for id_ in its.implementations:
            type_ = self.types[id_]
            impls[type_.type_name] = type_
        its.implementations = impls

    def _substitute_default_descendant(self, its):
        try:
            id_ = its.default_descendant
        except AttributeError:
            pass
        else:
            its.default_descendant = self.types[id_]

    def _substitute_key_type(self, its):
        for key, value in its.keys.items():
            value['type'] = self.types[value['type']]

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
        self.values = list_to_dict(data['values'], 'name')

    def _parse_filename(self, data):
        self.file_mode = data['file_mode']

    def _parse_array(self, data):
        self.__parse_range(data, default=[0, float('inf')])
        self.subtype = data['subtype']

    def _parse_record(self, data):
        self.type_name = data['type_name']
        self.keys = list_to_dict(data['keys'])
        for key in ['type_full_name', 'implements', 'reducible_to_key']:
            self.__parse_optional(data, key)

    def _parse_abstractrecord(self, data):
        self.implementations = data['implementations']
        self.__parse_optional(data, 'default_descendant')

    def __repr__(self):
        out = self.input_type + '{'
        if self.input_type == 'Record':
            out = out + self.type_name
        elif self.input_type == 'AbstractRecord':
            out = out + self.name
        elif self.input_type == 'Array':
            out = out + repr(self.subtype)
        elif self.input_type == 'Selection':
            out = out + self.name

        return out + '}'


def list_to_dict(list_, key_label='key'):
    """
    Transforms a list of dictionaries into a dictionary of dictionaries.

    Original dictionaries are assigned key specified in each of them
    by key_label.
    """
    dict_ = {}
    for item in list_:
        dict_[item[key_label]] = item
    return dict_

