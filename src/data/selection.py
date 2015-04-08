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
    selections = {}
    _allowed_kwargs = ['full_name', 'description']

    @staticmethod
    def selection(name):
        return Selection.selections[name]

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
            temp.value = int(temp.value)            # cast to integer
            self.values[temp.name] = temp

        # add reference to class dict for later retrival
        Selection.selections[name] = self


    def to_str(self, value):
        """
        Get str repr from int value.
        """
        for name, item in self.values.items():
            if item.value == value:
                return name
        raise KeyError

    def has(self, name):
        return (name in self.values)


class objectview(object):
    def __init__(self, d):
        self.__dict__ = d


