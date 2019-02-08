# -*- coding: utf-8 -*-
#
# Copyright © 2009-2010 CEA
# Pierre Raybaut
# Licensed under the terms of the CECILL License
# (see guidata/__init__.py for details)

"""
configtools
-----------

The ``guidata.configtools`` module provides configuration related tools.
"""

import os
import os.path as osp
import sys
import gettext

from qtpy import QtCore, QtWidgets, QtGui

from guidata.utils import get_module_path

IMG_PATH = []


def get_module_data_path(modname, relpath=None):
    """Return module *modname* data path
    Handles py2exe/cx_Freeze distributions"""
    datapath = getattr(sys.modules[modname], 'DATAPATH', '')
    if not datapath:
        datapath = get_module_path(modname)
        parentdir = osp.normpath(osp.join(datapath, osp.pardir))
        if osp.isfile(parentdir):
            # Parent directory is not a directory but the 'library.zip' file:
            # this is either a py2exe or a cx_Freeze distribution
            datapath = osp.abspath(osp.join(osp.join(parentdir, osp.pardir),
                                            modname))
    if relpath is not None:
        datapath = osp.abspath(osp.join(datapath, relpath))
    return datapath


def get_translation(modname, dirname=None):
    """Return translation callback for module *modname*"""
    if dirname is None:
        dirname = modname
    # fixup environment var LANG in case it's unknown
    if "LANG" not in os.environ:
        import locale  # Warning: 2to3 false alarm ('import' fixer)
        lang = locale.getdefaultlocale()[0]
        if lang is not None:
            os.environ["LANG"] = lang
    try:
        _trans = gettext.translation(modname, get_module_locale_path(dirname),
                                     codeset="utf-8")
        lgettext = _trans.lgettext
        return lgettext
    except IOError as _e:
        return lambda x: x


def get_module_locale_path(modname):
    """Return module *modname* gettext translation path"""
    localepath = getattr(sys.modules[modname], 'LOCALEPATH', '')
    if not localepath:
        localepath = get_module_data_path(modname, relpath="locale")
    return localepath


def add_image_path(path, subfolders=True):
    """Append image path (opt. with its subfolders) to global list IMG_PATH"""
    global IMG_PATH
    IMG_PATH.append(path)
    if subfolders:
        for fileobj in os.listdir(path):
            pth = osp.join(path, fileobj)
            if osp.isdir(pth):
                IMG_PATH.append(pth)


def add_image_module_path(modname, relpath, subfolders=True):
    """
    Appends image data path relative to a module name.
    Used to add module local data that resides in a module directory
    but will be shipped under sys.prefix / share/ ...

    modname must be the name of an already imported module as found in
    sys.modules
    """
    add_image_path(get_module_data_path(modname, relpath=relpath), subfolders)


def get_image_file_path(name, default="not_found.png"):
    """
    Return the absolute path to image with specified name
    name, default: filenames with extensions
    """
    for pth in IMG_PATH:
        full_path = osp.join(pth, name)
        if osp.isfile(full_path):
            return osp.abspath(full_path)
    if default is not None:
        try:
            return get_image_file_path(default, None)
        except RuntimeError:
            raise RuntimeError("Image file %r not found" % name)
    else:
        raise RuntimeError()


def get_icon(name, default="not_found.png"):
    """
    Construct a QIcon from the file with specified name
    name, default: filenames with extensions
    """
    return QtGui.QIcon(get_image_file_path(name, default))


def get_image_label(name, default="not_found.png"):
    """
    Construct a QLabel from the file with specified name
    name, default: filenames with extensions
    """
    label = QtWidgets.QLabel()
    pixmap = QtGui.QPixmap(get_image_file_path(name, default))
    label.setPixmap(pixmap)
    return label


def get_image_layout(imagename, text="", tooltip="", alignment=QtCore.Qt.AlignLeft):
    """
    Construct a QHBoxLayout including image from the file with specified name,
    left-aligned text [with specified tooltip]
    Return (layout, label)
    """
    layout = QtWidgets.QHBoxLayout()
    if alignment in (QtCore.Qt.AlignCenter, QtCore.Qt.AlignRight):
        layout.addStretch()
    layout.addWidget(get_image_label(imagename))
    label = QtWidgets.QLabel(text)
    label.setToolTip(tooltip)
    layout.addWidget(label)
    if alignment in (QtCore.Qt.AlignCenter, QtCore.Qt.AlignLeft):
        layout.addStretch()
    return (layout, label)
