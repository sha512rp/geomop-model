# -*- coding: utf-8 -*-
"""
GeomMop Model data structure

@author: Tomas Krizek
"""


import demjson
import re
import pprint


class FileHandler:
    pass


class ConFileHandler(FileHandler):
    pass


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
        
    def __getattr__(self, name):
        if name not in self._ref._value.keys():
            raise AttributeError

        return self._ref._value[name]

    def __getitem__(self, index):
        return self._ref._value[index]

    def __len__(self):
        return len(self._ref._value)

    def __iter__(self):
        for key, value in self._ref._value.items():
            yield key, value

    def __contains__(self, key):
        return key in self._ref._value.keys()


def parse_format(filename):
    return demjson.decode_file(filename)


def parse_con(filename):
    json = open(filename).read()

    p = re.compile(r"\s?=\s?");      # TODO can I replace = simply like this?
    json = p.sub(':', json)

    return demjson.decode(json)


def main():
    pp = pprint.PrettyPrinter()
    con = parse_con("../data/con/flow_dirichlet.con")
    format = parse_format("../data/format/flow_1.8.2_input_format.json")

    # pp.pprint(format)


if __name__ == '__main__':
    main()


