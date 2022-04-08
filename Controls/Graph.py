from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import StyleInfo


class Graph(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.data = []

    # data should be a list of y values to be plotted along x axis
    # using a line chart
    def set_data(self, data: list[float]):
        if len(data) == 0:
            raise "Data is empty"
        self.data = data
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_objects(painter)
        painter.end()

    def draw_background(self, painter: QPainter):
        painter.setPen(QPen(StyleInfo.color_background, StyleInfo.pen_width, Qt.SolidLine))
        painter.setBrush(QBrush(StyleInfo.color_background, Qt.SolidPattern))
        painter.drawRect(0, 0, self.width(), self.height())

    def draw_horizontal_gridlines(self, painter: QPainter):
        painter.setPen(QPen(StyleInfo.color_grid_line, StyleInfo.pen_width, Qt.SolidLine))
        for i in range(1, StyleInfo.num_horizontal_gridlines):
            x1 = 0
            x2 = self.width()
            y1 = i * int(self.height() / StyleInfo.num_horizontal_gridlines)
            y2 = y1
            painter.drawLine(x1, y1, x2, y2)

    def plot_lines(self, painter: QPainter):
        if len(self.data) > 0:
            maximum = max(self.data)
            minimum = min(self.data)
            diff = maximum - minimum
            num_points = len(self.data)
            for i in range(num_points - 1):
                painter.setPen(QPen(Qt.white, StyleInfo.pen_width, Qt.SolidLine))
                x1 = int(i * (self.width() / num_points))
                y1 = self.height() - int(((self.data[i] - minimum) / diff) * self.height())
                x2 = int((i + 1) * (self.width() / num_points))
                y2 = self.height() - int(((self.data[i + 1] - minimum) / diff) * self.height())
                painter.drawLine(x1, y1, x2, y2)

    def draw_objects(self, painter: QPainter):
        #  draw background
        self.draw_background(painter)
        self.draw_horizontal_gridlines(painter)
        self.plot_lines(painter)
