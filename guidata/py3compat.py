# -*- coding: utf-8 -*-
#
# Copyright © 2012-2013 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see spyderlib/__init__.py for details)

"""
guidata.py3compat (exact copy of spyderlib.py3compat)
-----------------------------------------------------

Transitional module providing compatibility functions intended to help
migrating from Python 2 to Python 3.

This module should be fully compatible with:
    * Python >=v2.6
    * Python 3
"""


def is_text_string(obj):
    """Return True if `obj` is a text string, False if it is anything else,
    like binary data (Python 3) or QString (Python 2, PyQt API #1)"""
    # Python 3
    return isinstance(obj, str)


def is_unicode(obj):
    """Return True if `obj` is unicode"""
    # Python 3
    return isinstance(obj, str)


def to_text_string(obj, encoding=None):
    """Convert `obj` to (unicode) text string"""
    # Python 3
    if encoding is None:
        return str(obj)
    elif isinstance(obj, str):
        # In case this function is not used properly, this could happen
        return obj
    else:
        return str(obj, encoding)


def cmp(a, b):
    return (a > b) - (a < b)
