# -*- coding: utf-8 -*-
#
# Copyright © 2009-2010 CEA
# Pierre Raybaut
# Licensed under the terms of the CECILL License
# (see guidata/__init__.py for details)

"""
RotatedLabel test

RotatedLabel is derived from QLabel: it provides rotated text display.
"""

from __future__ import unicode_literals

from qtpy.QtWidgets import QFrame, QGridLayout
from qtpy.QtCore import Qt
from guidata.qtwidgets import RotatedLabel

SHOW = True  # Show test in GUI-based test launcher


class Frame(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        layout = QGridLayout()
        self.setLayout(layout)
        angle = 0
        for row in range(7):
            for column in range(7):
                layout.addWidget(RotatedLabel("Label %03d°" % angle,
                                              angle=angle, color=Qt.blue,
                                              bold=True),
                                 row, column, Qt.AlignCenter)
                angle += 10


if __name__ == '__main__':
    from qtpy.QtWidgets import QApplication
    import sys
    app = QApplication([])
    frame = Frame()
    frame.show()
    sys.exit(app.exec_())
