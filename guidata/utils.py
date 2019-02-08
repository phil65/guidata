# -*- coding: utf-8 -*-
#
# Copyright © 2009-2010 CEA
# Pierre Raybaut
# Licensed under the terms of the CECILL License
# (see guidata/__init__.py for details)

# pylint: disable=C0103

"""
utils
-----

The ``guidata.utils`` module provides various utility helper functions
(pure python).
"""

import sys
import time
import os.path as osp
import locale  # Warning: 2to3 false alarm ('import' fixer)

from guidata.py3compat import (is_unicode, to_text_string, is_text_string)


def min_equals_max(min, max):
    """
    Return True if minimium value equals maximum value
    Return False if not, or if maximum or minimum value is not defined
    """
    return min is not None and max is not None and min == max


def pairs(iterable):
    """A simple generator that takes a list and generates
    pairs [ (l[0],l[1]), ..., (l[n-2], l[n-1])]
    """
    iterator = iter(iterable)
    first = next(iterator)
    while True:
        second = next(iterator)
        yield (first, second)
        first = second


def add_extension(item, value):
    """Add extension to filename
    `item`: data item representing a file path
    `value`: possible value for data item"""
    value = to_text_string(value)
    formats = item.get_prop("data", "formats")
    if len(formats) == 1 and formats[0] != '*':
        if not value.endswith('.' + formats[0]) and len(value) > 0:
            return value + '.' + formats[0]
    return value


def bind(fct, value):
    """
    Returns a callable representing the function 'fct' with it's
    first argument bound to the value

    if g = bind(f,1) and f is a function of x,y,z
    then g(y,z) will return f(1,y,z)
    """
    def callback(*args, **kwargs):
        return fct(value, *args, **kwargs)
    return callback


def trace(fct):
    """A decorator that traces function entry/exit
    used for debugging only
    """
    from functools import wraps

    @wraps(fct)
    def wrapper(*args, **kwargs):
        """Tracing function entry/exit (debugging only)"""
        print("enter:", fct.__name__)
        res = fct(*args, **kwargs)
        print("leave:", fct.__name__)
        return res
    return wrapper


def decode_fs_string(string):
    """Convert string from file system charset to unicode"""
    charset = sys.getfilesystemencoding()
    if charset is None:
        charset = locale.getpreferredencoding()
    return string.decode(charset)


def utf8_to_unicode(string):
    """Convert UTF-8 string to Unicode"""
    if not is_text_string(string):
        string = to_text_string(string)
    if not is_unicode(string):
        try:
            string = to_text_string(string, "utf-8")
        except UnicodeDecodeError:
            # This is border line... but we admit here string which has been
            # erroneously encoded in file system charset instead of UTF-8
            string = decode_fs_string(string)
    return string


# Findout the encoding used for stdout or use ascii as default
STDOUT_ENCODING = "ascii"
if hasattr(sys.stdout, "encoding"):
    if sys.stdout.encoding:
        STDOUT_ENCODING = sys.stdout.encoding


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


class Timer(object):
    """MATLAB-like timer: tic, toc"""

    def __init__(self):
        self.t0_dict = {}

    def tic(self, cat):
        """Starting timer"""
        print(">", cat)
        self.t0_dict[cat] = time.clock()

    def toc(self, cat, msg="delta:"):
        """Stopping timer"""
        print("<", cat, ":", msg, time.clock() - self.t0_dict[cat])

_TIMER = Timer()
tic = _TIMER.tic
toc = _TIMER.toc


def get_module_path(modname):
    """Return module *modname* base path"""
    module = sys.modules.get(modname, __import__(modname))
    return osp.abspath(osp.dirname(module.__file__))
