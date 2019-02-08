# -*- coding: utf-8 -*-
#
# Copyright © 2009-2010 CEA
# Pierre Raybaut
# Licensed under the terms of the CECILL License
# (see guidata/__init__.py for details)

"""
qthelpers
---------

The ``guidata.qthelpers`` module provides helper functions for developing
easily Qt-based graphical user interfaces.
"""

from qtpy.QtGui import (QColor, QIcon, QKeySequence)
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (QToolButton, QMenu, QPushButton, QStyle,
                            QWidget, QGroupBox, QAction)

# Local imports:
from guidata.py3compat import is_text_string


def text_to_qcolor(text):
    """Create a QColor from specified string"""
    color = QColor()
    if not is_text_string(text):  # testing for QString (PyQt API#1)
        text = str(text)
    if text.startswith('#') and len(text) == 7:
        correct = '#0123456789abcdef'
        for char in text:
            if char.lower() not in correct:
                return color
    elif text not in list(QColor.colorNames()):
        return color
    color.setNamedColor(text)
    return color


def get_std_icon(name, size=None):
    """
    Get standard platform icon
    Call 'show_std_icons()' for details
    """
    if not name.startswith('SP_'):
        name = 'SP_' + name
    icon = QWidget().style().standardIcon(getattr(QStyle, name))
    if size is None:
        return icon
    else:
        return QIcon(icon.pixmap(size, size))
