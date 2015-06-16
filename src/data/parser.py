# -*- coding: utf-8 -*-
"""
GeomMop configuration file parsers

This file contains the parsing functions for configuration files of Flow123d.
Currently supports .con format (as specified by Flow123d manual v1.8.2).

Future support for .yaml files for Flow123d v2 is planned.

@author: Tomas Krizek
"""

import demjson
import re
from copy import copy

from . import model


def parse_con(filename):
    """
    Parses a configuration file of Flow123d in .con format with given filename.
    If the input file includes references, they are resolved and represented
    by actual python references in the output.

    Returns the root of the resulting tree DataNode structure.
    """
    con = open(filename).read()
    data = _decode_con(con)
    _resolve_references(data)
    return data


def _resolve_references(data):
    """
    Resolves references in data. Replaces REF keys with actual Python
    references.
    """
    refs = _extract_references(data)

    while len(refs) > 0:
        length = len(refs)
        for path, ref_path in copy(refs).items():
            if not ref_path.startswith('/'):  # relative path
                ref_path = path + '/' + ref_path
            referred_to = model.get(data, ref_path)
            if referred_to is None:
                continue
            model.set(data, path, referred_to)
            del refs[path]
        if length == len(refs):
            # no reference removed -> impossible to resolve references
            raise Exception("Can not resolve references.")


def _decode_con(con):
    """Reads .con format and returns read data in form of dicts and lists."""
    pattern = re.compile(r"\s?=\s?")  # TODO can I replace = simply like this?
    con = pattern.sub(':', con)
    return demjson.decode(con)


def _extract_references(data):
    """
    Crawl through the data and find all REF keys.

    Returns a dictionary of their locations and where they point.
    """
    def find_reference(node, path='/'):
        try:  # is there a REF in this node?
            ref_path = node['REF']
        except Exception:
            pass
        else:  # extract reference
            refs[path] = ref_path
            return True

        # call for all children
        for child_path, child_node in model.children(node, path).items():
            if find_reference(child_node, child_path):
                # set the node to None
                model.set(node, model.path_to_keys(child_path).pop(), None)

        return False

    refs = {}
    find_reference(data)
    return refs
