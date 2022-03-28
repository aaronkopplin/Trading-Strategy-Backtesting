from PyQt5 import QtGui, QtWidgets, QtCore
from enum import Enum


class LayoutDirection(Enum):
    VERTICAL = 1
    HORIZONTAL = 2
    GRID = 3


class Panel(QtWidgets.QWidget):
    def __init__(self, direction: LayoutDirection):
        super(Panel, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        if direction == LayoutDirection.VERTICAL:
            self.panel_layout = QtWidgets.QVBoxLayout()
        elif direction == LayoutDirection.HORIZONTAL:
            self.panel_layout = QtWidgets.QHBoxLayout()
        elif direction == LayoutDirection.GRID:
            self.panel_layout = QtWidgets.QGridLayout()
        self.panel_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.panel_layout)

    def addWidget(self, w: QtWidgets.QWidget):
        self.panel_layout.addWidget(w)