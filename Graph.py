from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime
from Candle import Candle


class Graph(QtWidgets.QWidget):
    def __init__(self, candles: list):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.candles = candles
        self.candle_bodies = []
        self.setMouseTracking(True)
        self.draw_cursor = True
        self.mouse_x = 0
        self.mouse_y = 0
        self.global_min = 0
        self.global_max = 0

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.draw_cursor = True

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.draw_cursor = False
        self.update()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouse_x = a0.x()
        self.mouse_y = a0.y()
        self.update()

    def find_candle(self, x: float) -> Candle:
        for rect in self.candle_bodies:
            # and y >= rect["y"] and y <= rect["y"] + rect["h"]
            if rect["x"] <= x <= (rect["x"] + rect["w"]):
                return rect["candle"]

    def convert_y_to_price(self, y: int) -> float:
        return self.global_min + ((self.height() - y) / self.height() * (self.global_max - self.global_min))

    def convert_price_to_y(self, price: float) -> int:
        return self.height() - int(((price - self.global_min) / (self.global_max - self.global_min)) * self.height())

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_objects(painter)
        painter.end()

    def draw_objects(self, painter: QPainter):
        self.global_min = min([can.lower_band for can in self.candles if can.lower_band != 0])
        self.global_max = max([can.upper_band for can in self.candles if can.upper_band != 0])
        self.candle_bodies.clear()
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        # draw candle bodies
        candle_width = self.width() / len(self.candles)
        for i in range(len(self.candles)):
            # draw wicks
            painter.setPen(QPen(Qt.black))
            x1 = (i * candle_width) + (candle_width / 2)
            y1 = self.calc_y1(self.candles[i], self.global_max, self.global_min)
            x2 = x1
            y2 = self.calc_y2(self.candles[i], self.global_max, self.global_min)
            painter.drawLine(x1, y1, x2, y2)

            # draw candle bodies
            if self.candles[i].close >= self.candles[i].open:
                painter.setPen(QPen(Qt.darkGreen, 1, Qt.SolidLine))
                painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            else:
                painter.setPen(QPen(Qt.darkRed, 1, Qt.SolidLine))
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))

            x = i * candle_width
            y = self.calc_y(self.candles[i], self.global_max, self.global_min)
            w = candle_width
            h = self.calc_candle_height(self.candles[i], self.global_max, self.global_min)
            painter.drawRect(x, y, w, h)
            self.candle_bodies.append({"x": x, "y": y, "w": w, "h": h, "candle": self.candles[i]})

            # draw bollinger bands

            if i > 1:
                # upper band
                painter.setPen(QPen(Qt.blue))
                x1 = ((i-1) * candle_width) + (candle_width / 2)
                y1 = self.convert_price_to_y(self.candles[i-1].upper_band)
                x2 = (i * candle_width) + (candle_width / 2)
                y2 = self.convert_price_to_y(self.candles[i].upper_band)
                if self.candles[i-1].upper_band != 0 and self.candles[i].upper_band != 0:
                    painter.drawLine(QLine(int(x1), y1, int(x2), y2))

                # simple moving average
                painter.setPen(QPen(Qt.darkMagenta))
                x1 = ((i - 1) * candle_width) + (candle_width / 2)
                y1 = self.convert_price_to_y(self.candles[i - 1].sma)
                x2 = (i * candle_width) + (candle_width / 2)
                y2 = self.convert_price_to_y(self.candles[i].sma)
                if self.candles[i - 1].sma != 0 and self.candles[i].sma != 0:
                    painter.drawLine(QLine(int(x1), y1, int(x2), y2))

                # lower band
                painter.setPen(QPen(Qt.darkCyan))
                x1 = ((i - 1) * candle_width) + (candle_width / 2)
                y1 = self.convert_price_to_y(self.candles[i - 1].lower_band)
                x2 = (i * candle_width) + (candle_width / 2)
                y2 = self.convert_price_to_y(self.candles[i].lower_band)
                if self.candles[i - 1].lower_band != 0 and self.candles[i].lower_band != 0:
                    painter.drawLine(QLine(int(x1), y1, int(x2), y2))

        if self.draw_cursor:
            #  draw price, datetime next to cursor
            date = self.find_candle(self.mouse_x).date_time
            painter.setPen(QPen(Qt.black))
            painter.setFont(QFont("arial"))
            price = self.convert_y_to_price(self.mouse_y)
            painter.drawText(QPoint(int(self.mouse_x) + 5, int(self.mouse_y) - 5),
                             "(" + str('${:,.2f}'.format(round(price, 2))) + ", " + str(date) + ")")

            # draw cursor dashed lines
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

