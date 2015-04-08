# -*- coding: utf-8 -*-
"""
SelectionFactory for generating enums

@author: Tomas Krizek
"""

import copy


class Selection:
    """
        Stores selection type and its values.
    """
    selections = {}
    _allowed_kwargs = ['full_name', 'description']

    @staticmethod
    def selection(name):
        return Selection.selections[name]

    def __init__(self, name, options, **kwargs):
        self.options = copy.copy(options)
        Selection.selections[name] = self

        for name in Selection._allowed_kwargs:
            try:
                self.__setattr__(name, kwargs[name])
            except:
                pass

    def to_int(self, name):
        """
        Get int value from str repr.
        """
        return self.options[name]

    def to_str(self, item):
        """
        Get str repr from int value.
        """
        for name, value in self.options.items():
            if value == item:
                return name
        raise KeyError

