from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyleOption, QStyle
from PyQt5 import QtGui
from Controls.LayoutDirection import LayoutDirection
import StyleInfo
from Controls.VerticalLayout import VerticalLayout
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt
from overrides import overrides


class ComboBox(QtWidgets.QComboBox):
    def __init__(self):
        super(QtWidgets.QComboBox, self).__init__()
