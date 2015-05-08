# -*- coding: utf-8 -*-
"""
GeomMop Model data structure

@author: Tomas Krizek
"""


import demjson
import re
import pprint
from copy import copy


def parse_con(filename):
    return ConFileHandler.parse(filename)


class ConFileHandler:

    @staticmethod
    def parse(filename):
        con = open(filename).read()
        data = ConFileHandler._decode_con(con)
        return ConFileHandler._parse_json(data)

    @staticmethod
    def _parse_json(data):
        refs = ConFileHandler._extract_references(data)
        root = DataNode(data)
        while len(refs) > 0:
            length = len(refs)
            for path, ref_path in copy(refs).items():
                try:
                    node = root.get(path)
                    if ref_path.startswith('/'):  # absolute ref
                        node.ref = root.get(ref_path)
                    else:  # relative ref
                        node.ref = node.get(ref_path)
                except LookupError:
                    continue
                else: del refs[path]
            if length == len(refs):
                # no reference removed -> impossible to resolve references
                raise ReferenceError("Can not resolve references.")
        return root

    @staticmethod
    def _decode_con(con):
        p = re.compile(r"\s?=\s?");  # TODO can I replace = simply like this?
        con = p.sub(':', con)
        return demjson.decode(con)

    @staticmethod
    def _extract_references(json):
        def crawl(data, path):
            if isinstance(data, dict):
                try:
                    ref_path = data['REF']
                except KeyError:
                    pass
                else:
                    refs[path] = ref_path
                    del data['REF']
                # crawl for all keys
                for key, value in data.items():
                    crawl(value, path + '/' + key)
            elif isinstance(data, list):
                # crawl for all records
                for i, item in enumerate(data):
                    crawl(item, path + '/' + str(i))

        refs = {}
        crawl(json, '')
        return refs


class YamlFileHandler:
    pass


class DataNode:

    def circular_check(fn):
        def inner(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except RuntimeError:
                raise ReferenceError("Circular reference detected!")
        return inner

    @property
    @circular_check
    def value(self):
        ref = self._ref
        if ref == ref._ref:
            # reference points to itself -> end-point value
            return ref._value
        else:
            # multi-level reference, resolve recursively
            return ref.value

    @value.setter
    @circular_check
    def value(self, value):
        ref = self._ref
        if ref == ref._ref:
            # reference points to itself -> end-point value
            ref._value = value
        else:
            # multi-level reference, resolve recursively
            ref.value = value

    @property
    def ref(self):
        if self._ref == self:
            return None
        return self._ref

    @ref.setter
    def ref(self, value):
        if value is None:
            value = self
        self._ref = value

    @property
    def path(self):
        try:
            path = self.parent.path
        except AttributeError:
            path = ''
        if not path.endswith('/'):  # ensure only single slash
            path = path + '/'
        return path + self.name

    def __init__(self, data, parent=None, name=''):
        self._ref = self
        self.parent = parent
        self.name = name
        self._initialize_value(data)

    def _initialize_value(self, data):
        if isinstance(data, dict):
            self.value = {}
            for key, value in data.items():
                self.value[key] = self._create_child_node(value, key)
        elif isinstance(data, list):
            self.value = []
            for i, item in enumerate(data):
                self.value.append(self._create_child_node(item, str(i)))
        else:
            self.value = data

    def _create_child_node(self, data, name):
        """
        Creates a child DataNode instance. If provided data is already
        a DataNode, it will use the existing instance and change its
        position in the tree by manipulating parent and name.
        """
        if isinstance(data, DataNode):
            data.parent = self
            data.name = name
            return data
        else:
            return DataNode(data, self, name)

    def get(self, path):
        """
        Returns node at specified path.

        """
        if path.startswith(self.path):  # absolute path
            path = path[len(self.path):]
        elif path.startswith('/'):  # absolute path with different location
            raise LookupError("Can't resolve '" + path + 
                "' from node " + self.path)
        node = self
        for key in path.split('/'):
            if not key or key == '.':
                continue
            elif key == '..':
                node = node.parent
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

    def __repr__(self):
        return 'DataNode(' + self.path + \
            ((' (ref ' + str(self._ref) + ')') if self._ref != self 
            else '') + ')'


class ReferenceError(Exception):
    def __init__(self, message):
        super(ReferenceError, self).__init__(message)

