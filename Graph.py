from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Candle import Candle


class Graph(QtWidgets.QWidget):
    def __init__(self, candles: list):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.candles = candles
        self.candle_bodies = []
        self.setMouseTracking(True)
        self.mouse_x = 0
        self.mouse_y = 0

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouse_x = a0.x()
        self.mouse_y = a0.y()
        self.update()
        # for rect in self.candle_bodies:
        #     if (x >= rect["x"] and x <= rect["x"] + rect["w"] and y >= rect["y"] and y <= rect["y"] + rect["h"]):
        #         print(rect["candle"].open, rect["candle"].high, rect["candle"].low, rect["candle"].close)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_objects(painter)
        painter.end()

    def draw_objects(self, painter: QPainter):
        global_min = min([can.low for can in self.candles])
        global_max = max([can.high for can in self.candles])

        # draw candle bodies
        candle_width = self.width() / len(self.candles)
        for i in range(len(self.candles)):
            # draw wicks
            painter.setPen(QPen(Qt.black))
            x1 = (i * candle_width) + (candle_width / 2)
            y1 = self.calc_y1(self.candles[i], global_max, global_min)
            x2 = x1
            y2 = self.calc_y2(self.candles[i], global_max, global_min)
            painter.drawLine(x1, y1, x2, y2)

            # draw candle bodies
            if self.candles[i].close >= self.candles[i].open:
                painter.setPen(QPen(Qt.darkGreen, 1, Qt.SolidLine))
                painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            else:
                painter.setPen(QPen(Qt.darkRed, 1, Qt.SolidLine))
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))

            x = i * candle_width
            y = self.calc_y(self.candles[i], global_max, global_min)
            w = candle_width
            h = self.calc_candle_height(self.candles[i], global_max, global_min)
            painter.drawRect(x, y, w, h)
            self.candle_bodies.append({"x": x, "y": y, "w": w, "h": h, "candle": self.candles[i]})

        painter.setPen(QPen(Qt.black, 1, Qt.DashLine))
        painter.drawLine(0, self.mouse_y, self.width(), self.mouse_y)
        painter.drawLine(self.mouse_x, 0, self.mouse_x, self.height())

    def calc_y2(self, candle: Candle, global_max: float, global_min: float) -> float:
        percent_of_screen = (candle.low - global_min) / (global_max - global_min)
        pixel_height = percent_of_screen * self.height()
        distance_from_top = self.height() - pixel_height
        return distance_from_top

    def calc_y1(self, candle: Candle, global_max: float, global_min: float) -> float:
        percent_of_screen = (candle.high - global_min) / (global_max - global_min)
        pixel_height = percent_of_screen * self.height()
        distance_from_top = self.height() - pixel_height
        return distance_from_top

    def calc_y(self, candle: Candle, global_max: float, global_min: float) -> float:
        candle_top = max(candle.open, candle.close)
        percent_of_screen = (candle_top - global_min) / (global_max - global_min)
        pixel_height = percent_of_screen * self.height()
        distance_from_top = self.height() - pixel_height
        return distance_from_top

    def calc_candle_height(self, candle: Candle, global_max: float, global_min: float) -> float:
        h = max(candle.open, candle.close) - min(candle.open, candle.close)
        distance = global_max - global_min
        percent = h / distance
        return percent * self.height()

