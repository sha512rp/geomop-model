# -*- coding: utf-8 -*-
"""
GeomMop Model data structure

@author: Tomas Krizek
"""


import demjson
import re
import pprint


class FileHandler:
    def parse(self, filename):
        """Parse input file, returns ConData."""
        raise NotImplementedError


class ConFileHandler(FileHandler):
    def parse(self, filename):
        con = open(filename).read()
        raw = self._decode_con(con)
        # TODO replace ref

    def _decode_con(self, con):
        p = re.compile(r"\s?=\s?");  # TODO can I replace = simply like this?
        con = p.sub(':', con)
        return demjson.decode(con)


class YamlFileHandler(FileHandler):
    pass


class ConData:
    """
    Represents one node in con data structure.

    Supports dot notation for records, indexing for arrays.

    Attributes:
        _value: Returns raw value (scalar, dict, list)
        _ref: Holds reference to use
    """

    def __init__(self, data):
        # TODO _path
        self._ref = self
        if isinstance(data, dict):
            self._value = {}
            for key, value in data.items():
                self._value[key] = ConData(value)
                # osetreni ref
        elif isinstance(data, list):
            self._value = []
            for item in data:
                self._value.append(ConData(item))
        else:
            self._value = data
        
    def __setattr__(self, name, value):
        if name == '_ref':
            try:  # important to delete _value for reference to work
                del self._value
            except AttributeError:
                pass
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self._ref, name, value)
        # _attr -> __dict__
        # attr -> _value

    def __getattr__(self, name):
        if name in self._ref.__dict__.keys():
            return self._ref.__dict__[name]
        elif name in self._ref._value.keys():
            return self._ref._value[name]
        else:
            raise AttributeError
        # TODO works, isn't it too complicated?
        # issues with _ attributes, i.e. _its
        # _its has to be set before _ref -> getattr isn't called

        # maybe implement only for _value

    def __getitem__(self, index):
        return self._ref._value[index]

    def __len__(self):
        return len(self._ref._value)

    def __iter__(self):
        for key, value in self._ref._value.items():
            yield key, value

    def __contains__(self, key):
        return key in self._ref._value.keys()


class ConData2:
    def value():
        doc = "The value property. Uses reference to get/set value."
        def fget(self):
            return self._ref._value
        def fset(self, value):
            self._ref._value = value
        return locals()
    value = property(**value())

    def ref():
        doc = "The ref property. References another instance."
        def fget(self):
            if self._ref == self:
                return None
            return self._ref
        def fset(self, value):
            if value is None:
                value = self
            self._ref = value
        return locals()
    ref = property(**ref())

    def __init__(self, data, parent=None, key=''):
        self._ref = self
        self.parent = parent
        try:
            path = parent.path
        except AttributeError:
            path = ''
        else:
            if not path.endswith('/'):  # ensure only single slash
                path = path + '/'
        self.path = path + key

        if isinstance(data, dict):
            self.value = {}
            for key, value in data.items():
                self.value[key] = ConData2(value, self, key)
        elif isinstance(data, list):
            self.value = []
            for i, item in enumerate(data):
                self.value.append(ConData2(item, self, str(i)))
        else:
            self.value = data

    def get(self, path):
        """Returns node at specified path."""
        if path.startswith(self.path):  # absolute path
            path = path[len(self.path):]
        elif path.startswith('/'):  # absolute path with different location
            raise LookupError("Can't resolve '" + path + 
                "' from node '" + self.path + "'")
        node = self
        for key in path.split('/'):
            if not key:
                continue
            try:
                key = int(key)
            except ValueError:
                pass
            try:
                node = node.value[key]
            except LookupError:
                raise LookupError("Node '" + 
                    str(key) + "' does not exist in " + node.path)
        return node


def main():
    pp = pprint.PrettyPrinter()
    con = parse_con("../data/con/flow_dirichlet.con")
    format = parse_format("../data/format/flow_1.8.2_input_format.json")

    # pp.pprint(format)


if __name__ == '__main__':
    main()


