# -*- coding: utf-8 -*-
"""
GeomMop Model data structure

@author: Tomas Krizek
"""


import demjson
import re
import pprint


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
