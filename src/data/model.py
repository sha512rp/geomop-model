# -*- coding: utf-8 -*-
"""
GeomMop configuration file data structure

Data structure of configuration files forms a tree. Each node has
access to its descendats, so only the reference to the root node is
needed to access all the nodes in the tree.

Original data consist of records, arrays and scalar values. A node is
constructed for each scalar, item in array and key in record. Each node
has a path that indicates its position in the tree.

@author: Tomas Krizek
"""


def path_to_keys(path):
    """
    Translates path to a sequence of keys.
    resolves .. and .
    e.g.: '/path/to/not_this/../but_this/./1'
    would return ('path', 'to', 'but_this', 1)
    """
    keys = []
    for key in path.split('/'):
        if not key or key == '.':
            continue
        elif key == '..':
            # move up -> remove parent
            if not keys:
                raise Exception('Invalid path: ' + str(path))
            keys.pop()
        else:
            try:  # convert to integer if possible
                key = int(key)
            except ValueError:
                pass
            keys.append(key)

    return tuple(keys)


def get(node, path):
    """
    Retrieves node at the specified path.
    If the path does not exist, returns None.
    """
    try:
        keys = path_to_keys(path)
    except Exception:
        return None
    return get_by_keys(node, keys)


def get_by_keys(node, keys):
    """
    Retrives node using the specified keys.
    If the path does not exist, returns None.
    """
    value = node
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key, None)
        elif isinstance(value, list):
            try:
                key = int(key)
                value = value[key]
            except Exception:
                value = None
                break
        else:
            value = None
            break
    return value


def children(node):
    """
    Returns children of this node.

    dict for Record,
    list for Array
    """
    pass