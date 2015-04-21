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

    def __init__(self, json_data):
        """Initialize the class by parsing ITS from JSON data."""
        self.types = {}
        self.name_collisions = []
        self.root_id = json_data[0]['id']      # set root type
        for item in json_data:
            its = InputTypeSpecification(item)
            self.types[its.id] = its  # register by id
            try:
                name = its.name
            except AttributeError:
                pass  # its does not have to have a name
            else:  # register by name
                # try to remove the name from dict
                if self.types.pop(its.name, None) is not None:
                    # name exists in dict -> it is removed and name
                    # is added to collisions
                    self.name_collisions = its.name
                else:
                    # removal failed, name is not in dict
                    # if name is not a collision, register it
                    if name not in self.name_collisions:
                        self.types[its.name] = its

    def get_its(self, key):
        """
        Return ITS for given id, name or path.

        id: randomly assigned hex number (from JSON file)
        name: human readable class name
        path: points to any node in the tree, starts with /
        """
        try:  # assume id or name
            return self.types[key]
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
        self.values = SelectionValues(data['values'])

    def _parse_filename(self, data):
        self.file_mode = data['file_mode']

    def _parse_array(self, data):
        self.min = data['range'][0]
        self.max = data['range'][1]
        self.subtype = data['subtype']


class SelectionValues:
    """
        Stores selection values.

        Supports iteration, length and access through dot notation.
    """

    class objectview(object):
        def __init__(self, d):
            self.__dict__ = d

    def __init__(self, data):
        for item in data:
            value = SelectionValues.objectview(copy.copy(item))
            self.__dict__[value.name] = value

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        for name in self.__dict__.keys():
            yield self.__dict__[name]

    def __contains__(self, item):
        return item in self.__dict__.keys()

