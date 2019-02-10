# -*- coding: utf-8 -*-
#
# Copyright © 2009-2010 CEA
# Pierre Raybaut
# Licensed under the terms of the CECILL License

"""
utils
-----

The ``guidata.utils`` module provides various utility helper functions
(pure python).
"""

import sys
import os.path as osp


def add_extension(item, value):
    """Add extension to filename
    `item`: data item representing a file path
    `value`: possible value for data item"""
    value = str(value)
    formats = item.get_prop("data", "formats")
    if len(formats) == 1 and formats[0] != '*':
        if not value.endswith('.' + formats[0]) and len(value) > 0:
            return value + '.' + formats[0]
    return value


def update_dataset(dest, source, visible_only=False):
    """
    Update `dest` dataset items from `source` dataset

    dest should inherit from DataSet, whereas source can be:
        * any Python object containing matching attribute names
        * or a dictionary with matching key names

    For each DataSet item, the function will try to get the attribute
    of the same name from the source.

    visible_only: if True, update only visible items
    """
    for item in dest._items:
        key = item._name
        if hasattr(source, key):
            try:
                hide = item.get_prop_value("display", source, "hide", False)
            except AttributeError:
                # FIXME: Remove this try...except
                hide = False
            if visible_only and hide:
                continue
            setattr(dest, key, getattr(source, key))
        elif isinstance(source, dict) and key in source:
            setattr(dest, key, source[key])


def restore_dataset(source, dest):
    """
    Restore `dest` dataset items from `source` dataset

    This function is almost the same as update_dataset but requires
    the source to be a DataSet instead of the destination.

    Symetrically from update_dataset, `dest` may also be a dictionary.
    """
    for item in source._items:
        key = item._name
        value = getattr(source, key)
        if hasattr(dest, key):
            try:
                setattr(dest, key, value)
            except AttributeError:
                # This attribute is a property, skipping this iteration
                continue
        elif isinstance(dest, dict):
            dest[key] = value


def get_module_path(modname):
    """Return module *modname* base path"""
    module = sys.modules.get(modname, __import__(modname))
    return osp.abspath(osp.dirname(module.__file__))
