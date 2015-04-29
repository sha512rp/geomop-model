# -*- coding: utf-8 -*-
"""
GeomMop Model data structure

@author: Tomas Krizek
"""


import demjson
import re
import pprint


class ConFileHandler:
    def parse(self, filename):
        con = open(filename).read()
        raw = self._decode_con(con)
        # TODO replace ref

    def _decode_con(self, con):
        p = re.compile(r"\s?=\s?");  # TODO can I replace = simply like this?
        con = p.sub(':', con)
        return demjson.decode(con)


class YamlFileHandler:
    pass


class DataNode:
    @property
    def value(self):
        return self._ref._value

    @value.setter
    def value(self, value):
        self._ref._value = value

    @property
    def ref():
        if self._ref == self:
            return None
        return self._ref

    @ref.setter
    def ref(self, value):
        if value is None:
            value = self
        self._ref = value

    def __init__(self, data, parent=None, name=''):
        self._ref = self
        self.parent = parent
        self.path = self._generate_path(name)
        self._initialize_value(data)

    def _generate_path(self, name):
        try:
            path = self.parent.path
        except AttributeError:
            path = ''
        else:
            if not path.endswith('/'):  # ensure only single slash
                path = path + '/'
        return path + name

    def _initialize_value(self, data):
        if isinstance(data, dict):
            self.value = {}
            for key, value in data.items():
                self.value[key] = DataNode(value, self, key)
        elif isinstance(data, list):
            self.value = []
            for i, item in enumerate(data):
                self.value.append(DataNode(item, self, str(i)))
        else:
            self.value = data

    def get(self, path):
        """Returns node at specified path."""
        if path.startswith(self.path):  # absolute path
            path = path[len(self.path):]
        elif path.startswith('/'):  # absolute path with different location
            raise LookupError("Can't resolve '" + path + 
                "' from node " + self.path)
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


