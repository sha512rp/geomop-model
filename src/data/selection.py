# -*- coding: utf-8 -*-
"""
Selection class

@author: Tomas Krizek
"""

import copy
from collections import namedtuple


class Selection:
    """
        Stores selection type and its values.
    """
    _allowed_kwargs = ['full_name', 'description']

    def __init__(self, name, values, **kwargs):
        self.name = name

        # initialize additional arguments
        for arg in Selection._allowed_kwargs:
            try:
                self.__setattr__(arg, kwargs[arg])
            except:
                pass

        # initialize values dict
        self.values = {}
        for item in values:
            temp = objectview(copy.copy(item))      # copy to ensure no runtime changes
            self.values[temp.name] = temp

    def has(self, name):
        """
        Determines if name is a possible value of this selection.
        Case-insensitive.
        """
        return (name.lower() in [val.name.lower() for key, val \
            in self.values.items()])


class objectview(object):
    def __init__(self, d):
        self.__dict__ = d


