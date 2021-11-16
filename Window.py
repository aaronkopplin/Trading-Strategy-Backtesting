from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QBrush, QPen, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

from Candle import Candle


class Window(QMainWindow):
    def __init__(self, candles: list):
        super().__init__()
        self.title = "Trading Bot"
        self.top = 150
        self.left = 150
        self.width = 500
        self.height = 500
        self.vertical_lines = 10
        self.horizontal_lines = 10
        self.candles = candles
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def set_candles(self, painter: QPainter):
        global_min = min([can.low for can in self.candles])
        global_max = max([can.high for can in self.candles])

        # draw grid lines
        interval = float(self.height) / float(self.horizontal_lines)
        for i in range(self.horizontal_lines):
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QtCore.Qt.blue)
            painter.setBrush(QtCore.Qt.white)
            y = self.height - (interval * i)
            painter.drawLine(0, y, self.width, y)

        # draw candle bodies
        candle_width = self.width / len(self.candles)
        for i in range(len(self.candles)):
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
            print(x, y, w, h)
            painter.drawRect(x, y, w, h)

    def calc_y(self, candle: Candle, global_max: float, global_min: float) -> float:
        candle_top = max(candle.open, candle.close)
        percent_of_screen = (candle_top - global_min) / (global_max - global_min)
        pixel_height = percent_of_screen * self.height
        distance_from_top = self.height - pixel_height
        return distance_from_top

    def calc_candle_height(self, candle: Candle, global_max: float, global_min: float) -> float:
        h = max(candle.open, candle.close) - min(candle.open, candle.close)
        distance = global_max - global_min
        percent = h / distance
        return percent * self.height

    def paintEvent(self, event):
        painter = QPainter(self)
        # painter.begin(self)
        self.set_candles(painter)
        painter.end()


