# -*- coding: utf-8 -*-
"""
Contains format specification class and methods to parse it from JSON.

@author: Tomas Krizek
"""

class FormatSpecification:
    """
    Contains complete input type specification (ITS).

    Functions:
        - return ITS for any path in the tree structure
        - return default value for any path
    """

    def __init__(self, json_data):
        """Initialize the class by parsing ITS from JSON data."""
        self.types = {}
        self.root_id = json_data[0]['id']      # set root type
        for data in json_data:
            its = InputTypeSpecification(data)
            self.types[its.id] = its
            try:
                self.types[its.name] = its
            except AttributeError:
                pass

    def get_its(self, key):
        """Return ITS for given id or name."""
        return self.types[key]



class InputTypeSpecification:
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
        self.subtype = data['subtype']
