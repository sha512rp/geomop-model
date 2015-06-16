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

from copy import copy


def path_to_keys(path):
    """
    Translates path to a sequence of keys.
    resolves .. and .
    e.g.: '/path/to/not_this/../but_this/./1'
    would return ('path', 'to', 'but_this', 1)
    Returns None if path can not be resolved.
    """
    keys = []
    for key in str(path).split('/'):
        if not key or key == '.':
            continue
        elif key == '..':
            # move up -> remove parent
            if not keys:
                return None  # cannot move up, unable to resolve
            keys.pop()
        else:
            try:  # convert to integer if possible
                key = int(key)
            except ValueError:
                pass
            keys.append(key)

    return keys


def keys_to_path(keys, absolute=True):
    """
    Translate keys to a string representation of path.
    """
    if keys is None:
        return None

    path = '/'.join([str(key) for key in keys])
    if absolute:  # add leading slash
        path = '/' + path
    return path


def get(node, path):
    """
    Retrieves node at the specified path.
    If the path does not exist, returns None.
    """
    keys = path_to_keys(path)
    return get_by_keys(node, keys)


def set(node, path, value):
    """
    Sets a child node at the specified path to the given value.
    """
    keys = path_to_keys(path)
    if keys is None or not keys:
        raise Exception("Invalid path!")

    key_to_set = keys.pop()
    get_by_keys(node, keys)[key_to_set] = value


def get_by_keys(node, keys):
    """
    Retrives node using the specified keys.
    If the path does not exist, returns None.
    """
    value = node
    if keys is None:
        raise Exception('Invalid path!')

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


def children(node, path='/'):
    """
    Returns children of this node.
    Provide path to this node to generate correct absolute paths.
    Output dictionary contains paths and nodes.
    """
    keys = path_to_keys(path)

    def parse_children(data):
        children = {}
        for key, node in data:
            child_keys = list(keys)
            child_keys.append(key)
            child_path = keys_to_path(child_keys)
            children[child_path] = node
        return children

    if isinstance(node, dict):
        return parse_children(node.items())
    elif isinstance(node, list):
        return parse_children(enumerate(node))
    else:
        return {}
