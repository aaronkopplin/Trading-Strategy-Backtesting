from DataClasses.RGBA import RGBA
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Collection(list):
    def __init__(self, title: str, data: list, color: RGBA):
        super(Collection, self).__init__(data)
        self.color: RGBA = color
        self.title = title

    def get_qcolor(self):
        return QColor(self.color.r, self.color.g, self.color.b, self.color.a)
