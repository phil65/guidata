# -*- coding: utf-8 -*-
#
# Copyright © 2009-2010 CEA
# Pierre Raybaut
# Licensed under the terms of the CECILL License
# (see guidata/__init__.py for details)

"""
Reader and Writer for the serialization of DataSets into HDF5 files
"""

import sys
from uuid import uuid1

import h5py

from guidata.userconfigio import BaseIOHandler, WriterMixin


class H5Store(object):

    def __init__(self, filename):
        self.filename = filename
        self.h5 = None

    def open(self, mode="a"):
        """Open an hdf5 file"""
        if self.h5:
            return self.h5
        try:
            self.h5 = h5py.File(self.filename, mode=mode)
        except Exception:
            print(f"Error trying to load {self.filename} in mode {mode}",
                  file=sys.stderr)
            raise
        return self.h5

    def close(self):
        if self.h5:
            self.h5.close()
        self.h5 = None


class HDF5Handler(H5Store, BaseIOHandler):
    """Base HDF5 I/O Handler object"""

    def __init__(self, filename):
        super().__init__(filename)
        self.option = []

    def get_parent_group(self):
        parent = self.h5
        for option in self.option[:-1]:
            parent = parent.require_group(option)
        return parent


class HDF5Writer(HDF5Handler, WriterMixin):
    """Writer for HDF5 files"""

    def __init__(self, filename):
        super().__init__(filename)
        self.open("w")

    def write_any(self, val):
        group = self.get_parent_group()
        group.attrs[self.option[-1]] = val

    write_int = write_float = write_any

    def write_bool(self, val):
        self.write_int(int(val))

    def write_array(self, val):
        group = self.get_parent_group()
        group[self.option[-1]] = val

    write_sequence = write_any

    def write_none(self):
        group = self.get_parent_group()
        group.attrs[self.option[-1]] = ""

    def write_object_list(self, seq, group_name):
        """Write object sequence in group.
        Objects must implement the DataSet-like `serialize` method"""
        with self.group(group_name):
            if seq is None:
                self.write_none()
            else:
                ids = []
                for obj in seq:
                    guid = bytes(str(uuid1()), 'utf-8')
                    ids.append(guid)
                    with self.group(guid):
                        if obj is None:
                            self.write_none()
                        else:
                            obj.serialize(self)
                self.write(ids, 'IDs')


class HDF5Reader(HDF5Handler):
    """Reader for HDF5 files"""

    def __init__(self, filename):
        super().__init__(filename)
        self.open("r")

    def read(self, group_name=None, func=None, instance=None):
        """Read value within current group or group_name.

        Optional argument `instance` is an object which
        implements the DataSet-like `deserialize` method."""
        if group_name:
            self.begin(group_name)
        if instance is None:
            if func is None:
                func = self.read_any
            val = func()
        else:
            group = self.get_parent_group()
            if group_name in group.attrs:
                # This is an attribute (not a group), meaning that
                # the object was None when deserializing it
                val = None
            else:
                instance.deserialize(self)
                val = instance
        if group_name:
            self.end(group_name)
        return val

    def read_any(self):
        group = self.get_parent_group()
        value = group.attrs[self.option[-1]]
        if isinstance(value, bytes):
            return value.decode("utf-8")
        else:
            return value

    def read_bool(self):
        val = self.read_any()
        if val != '':
            return bool(val)

    def read_int(self):
        val = self.read_any()
        if val != '':
            return int(val)

    def read_float(self):
        val = self.read_any()
        if val != '':
            return float(val)

    def read_array(self):
        group = self.get_parent_group()
        return group[self.option[-1]][...]

    def read_sequence(self):
        group = self.get_parent_group()
        return list(group.attrs[self.option[-1]])

    def read_object_list(self, group_name, klass, progress_callback=None):
        """Read object sequence in group.
        Objects must implement the DataSet-like `deserialize` method.
        `klass` is the object class which constructor requires no argument.

        progress_callback: if not None, this function is called with
        an integer argument (progress: 0 --> 100). Function returns the
        `cancel` state (True: progress dialog has been canceled, False
        otherwise)
        """
        with self.group(group_name):
            try:
                ids = self.read('IDs', func=self.read_sequence)
            except ValueError:
                # None was saved instead of list of objects
                self.end('IDs')
                return
            seq = []
            count = len(ids)
            for idx, name in enumerate(ids):
                if progress_callback is not None:
                    if progress_callback(int(100 * float(idx) / count)):
                        break
                with self.group(name):
                    group = self.get_parent_group()
                    if name in group.attrs:
                        # This is an attribute (not a group), meaning that
                        # the object was None when deserializing it
                        obj = None
                    else:
                        obj = klass()
                        obj.deserialize(self)
                seq.append(obj)
        return seq
