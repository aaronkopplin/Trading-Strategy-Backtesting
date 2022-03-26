import csv
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import date, timedelta
from Candle import Candle
import yfinance
from PullData import read_candles
from datetime import datetime
from Strategy import Account, Trade
import StyleInfo


class Chart(QtWidgets.QWidget):
    def __init__(self, candles: list):
        super().__init__()
        self.ticker_symbol = "BTC-USD"
        self.setContentsMargins(0, 0, 0, 0)
        self.candles = candles
        self.last_candle = len(self.candles)
        self.first_candle = self.last_candle - self.min_zoom()
        self.global_min = self.min_candle_val()
        self.global_max = self.max_candle_val()
        self.candle_bodies = []
        self.setMouseTracking(True)
        self.draw_cursor = True
        self.mouse_x = 0
        self.mouse_y = 0
        self.candle_width = self.width() / self.num_candles_on_screen()
        self.mouse_prev_location = 0
        self.mouse_down = False

    def strategy_run_event(self, account: Account):
        trade: Trade
        for trade in account.trades:
            buy_can: Candle = self.candles[trade.buy_candle_index]
            buy_can.bought = True
            if trade.sell_candle_index:
                sell_can = self.candles[trade.sell_candle_index]
                sell_can.sold = True
        self.update()

    def min_zoom(self) -> int:
        return max(int(float(len(self.candles)) / float(10)), 1)

    def num_candles_on_screen(self):
        return self.last_candle - self.first_candle

    def run_query(self, begin: QDateTime, end: QDateTime, interval: str):
        start = f"{begin.date().year()}-{begin.date().month()}-{begin.date().day()}"
        end = f"{end.date().year()}-{end.date().month()}-{end.date().day()}"
        data = yfinance.download([self.ticker_symbol],
                                 start=start,
                                 end=end,
                                 interval=interval)
        if len(data) > 1:
            data.to_csv("data.csv")
            with open("last_query.csv", "w") as f:
                f.write("ticker_symbol,begin,end,interval\n")
                f.write(f"{self.ticker_symbol},{start},{end},{interval}")

            self.candles = read_candles()
            self.last_candle = len(self.candles)
            self.first_candle = self.last_candle - self.min_zoom()
            self.update()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouse_prev_location = a0.x()
        self.mouse_down = True

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouse_down = False

    def move_left(self, num_candles: int):
        while self.first_candle > 0 and self.num_candles_on_screen() >= self.min_zoom() and num_candles > 0:
            self.last_candle -= 1
            self.first_candle -= 1
            num_candles -= 1
        self.update()

    def move_right(self, num_candles: int):
        while self.last_candle < len(self.candles) and self.num_candles_on_screen() >= self.min_zoom() and num_candles > 0:
            self.first_candle += 1
            self.last_candle += 1
            num_candles -= 1
        self.update()

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.draw_cursor = True

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.draw_cursor = False
        self.update()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.mouse_down:
            if a0.x() > self.mouse_prev_location + self.candle_width:
                distance = a0.x() - self.mouse_prev_location
                num_candles = distance / self.candle_width
                self.move_left(int(num_candles))
                self.mouse_prev_location = a0.x()
            if a0.x() < self.mouse_prev_location - self.candle_width:
                distance = self.mouse_prev_location - a0.x()
                num_candles = distance / self.candle_width
                self.mouse_prev_location = a0.x()
                self.move_right(int(num_candles))
        self.mouse_x = a0.x()
        self.mouse_y = a0.y()
        self.update()

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        if a0.angleDelta().y() < 0:  # zoom out
            for i in range(self.min_zoom()):
                if self.num_candles_on_screen() < len(self.candles):
                    if self.first_candle > 0:
                        self.first_candle -= 1
                    elif self.last_candle < len(self.candles):
                        self.last_candle += 1

        if a0.angleDelta().y() > 0:  # zoom in
            for i in range(self.min_zoom()):
                if self.num_candles_on_screen() > self.min_zoom():
                    if self.first_candle < self.last_candle - self.min_zoom():
                        self.first_candle += 1
                    elif self.last_candle > self.first_candle + self.min_zoom():
                        self.last_candle -= 1

        self.update()

    def find_candle(self, x: float) -> Candle:
        for can in self.candle_bodies:
            if can.x <= x <= (can.x + can.w):
                return can

    def convert_y_to_price(self, y: int) -> float:
        return self.global_min + ((self.height() - y) / self.height() * (self.global_max - self.global_min))

    def convert_price_to_y(self, price: float) -> int:
        return self.height() - int(((price - self.global_min) / (self.global_max - self.global_min)) * self.height())

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_objects(painter)
        painter.end()

    def min_candle_val(self):
        cans = self.candles[self.first_candle:self.last_candle]
        lows = [can.low for can in cans if can.low != 0]
        lower_bands = [can.lower_band for can in cans if can.lower_band != 0]
        return min(lows + lower_bands)

    def max_candle_val(self):
        cans = self.candles[self.first_candle:self.last_candle]
        highs = [can.high for can in cans if can.high != 0]
        upper_bands = [can.upper_band for can in cans if can.upper_band != 0]
        return max(highs + upper_bands)

    def draw_objects(self, painter: QPainter):
        self.global_min = self.min_candle_val()
        self.global_max = self.max_candle_val()
        self.candle_bodies.clear()
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        #  draw background
        painter.setPen(QPen(StyleInfo.background_color, StyleInfo.pen_width, Qt.SolidLine))
        painter.setBrush(QBrush(StyleInfo.background_color, Qt.SolidPattern))
        painter.drawRect(0, 0, self.width(), self.height())

        #  draw horizontal gridlines
        painter.setPen(QPen(StyleInfo.gridline_color, StyleInfo.pen_width, Qt.SolidLine))
        for i in range(1, StyleInfo.num_horizontal_gridlines):
            x1 = 0
            x2 = self.width()
            y1 = i * int(self.height() / StyleInfo.num_horizontal_gridlines)
            y2 = y1
            painter.drawLine(x1, y1, x2, y2)

        # draw candle bodies
        self.candle_width = self.width() / self.num_candles_on_screen()
        for i in range(self.num_candles_on_screen()):
            curr_candle: Candle = self.candles[i + self.first_candle]
            prev_candle: Candle = self.candles[i + self.first_candle - 1]

            # draw wicks
            x1 = int((i * self.candle_width) + (self.candle_width / 2))
            y1 = int(self.calc_y1(curr_candle))
            x2 = int(x1)
            y2 = int(self.calc_y2(curr_candle))
            if curr_candle.close >= curr_candle.open:
                painter.setPen(QPen(StyleInfo.green_candle, StyleInfo.pen_width, Qt.SolidLine))
            else:
                painter.setPen(QPen(StyleInfo.red_candle, StyleInfo.pen_width, Qt.SolidLine))
            painter.drawLine(x1, y1, x2, y2)

            # draw grid lines
            if i % StyleInfo.num_candles_per_gridline == 0:
                painter.setPen(QPen(StyleInfo.gridline_color, StyleInfo.pen_width, Qt.SolidLine))
                painter.drawLine(x1, 0, x1, self.height())

            # dimensions for candle bodies
            x = int(i * self.candle_width)
            y = int(self.calc_y(curr_candle, self.global_max, self.global_min))
            w = int(self.candle_width)
            h = int(self.calc_candle_height(curr_candle, self.global_max, self.global_min))

            # if strategy has run and candle is bought or sold
            if curr_candle.bought:
                color = QColor(204, 255, 179, 75)
                painter.setPen(QPen(color, StyleInfo.pen_width, Qt.SolidLine))
                painter.setBrush(QBrush(color, Qt.SolidPattern))
                painter.drawRect(x, 0, w, self.height())
            if curr_candle.sold:
                color = QColor(255, 179, 179, 75)
                painter.setPen(QPen(color, StyleInfo.pen_width, Qt.SolidLine))
                painter.setBrush(QBrush(color, Qt.SolidPattern))
                painter.drawRect(x, 0, w, self.height())

            # draw candle bodies
            if curr_candle.close >= curr_candle.open:
                painter.setPen(QPen(StyleInfo.green_candle, StyleInfo.pen_width, Qt.SolidLine))
                painter.setBrush(QBrush(StyleInfo.background_color, Qt.SolidPattern))
            else:
                painter.setPen(QPen(StyleInfo.red_candle, StyleInfo.pen_width, Qt.SolidLine))
                painter.setBrush(QBrush(StyleInfo.red_candle, Qt.SolidPattern))

            painter.drawRect(x, y, w, h)
            curr_candle.x = x
            curr_candle.y = y
            curr_candle.w = w
            curr_candle.h = h
            self.candle_bodies.append(curr_candle)

            # draw bollinger bands
            if i > 1:
                # upper band
                painter.setPen(QPen(StyleInfo.bollinger_band_color, StyleInfo.pen_width, Qt.SolidLine))
                x1 = ((i-1) * self.candle_width) + (self.candle_width / 2)
                y1 = self.convert_price_to_y(prev_candle.upper_band)
                x2 = (i * self.candle_width) + (self.candle_width / 2)
                y2 = self.convert_price_to_y(curr_candle.upper_band)
                if prev_candle.upper_band != 0 and curr_candle.upper_band != 0:
                    painter.drawLine(QLine(int(x1), y1, int(x2), y2))

                # simple moving average
                painter.setPen(QPen(Qt.white, StyleInfo.pen_width, Qt.SolidLine))
                x1 = ((i - 1) * self.candle_width) + (self.candle_width / 2)
                y1 = self.convert_price_to_y(prev_candle.sma)
                x2 = (i * self.candle_width) + (self.candle_width / 2)
                y2 = self.convert_price_to_y(curr_candle.sma)
                if prev_candle.sma != 0 and curr_candle.sma != 0:
                    painter.drawLine(QLine(int(x1), y1, int(x2), y2))

                # lower band
                painter.setPen(QPen(StyleInfo.bollinger_band_color, StyleInfo.pen_width, Qt.SolidLine))
                x1 = ((i - 1) * self.candle_width) + (self.candle_width / 2)
                y1 = self.convert_price_to_y(prev_candle.lower_band)
                x2 = (i * self.candle_width) + (self.candle_width / 2)
                y2 = self.convert_price_to_y(curr_candle.lower_band)
                if prev_candle.lower_band != 0 and curr_candle.lower_band != 0:
                    painter.drawLine(QLine(int(x1), y1, int(x2), y2))

        if self.draw_cursor:
            #  draw price, datetime next to cursor
            can = self.find_candle(self.mouse_x)
            if can is not None:
                can_date = can.date_time
                painter.setPen(QPen(Qt.white))
                painter.setFont(QFont("arial", StyleInfo.font_size))
                price = f"Open: ${'{:,.2f}'.format(can.open)}, " \
                        f"High: ${'{:,.2f}'.format(can.high)}, " \
                        f"Low: ${'{:,.2f}'.format(can.low)}, " \
                        f"Close: ${'{:,.2f}'.format(can.close)}, "
                can_date = "Date: " + str(can_date)
                painter.drawText(QRectF(5, 5, self.width(), self.height()),
                                 Qt.AlignLeft|Qt.AlignTop,
                                 price + can_date)

                # draw cursor dashed lines
                painter.setPen(QPen(StyleInfo.cursor_color, StyleInfo.pen_width, Qt.DashLine))
                add_height = 0
                if not can.green():
                    add_height = can.h
                painter.drawLine(0, can.y + add_height, self.width(), can.y + add_height)  # horiz
                painter.drawLine(can.x + int(can.w / 2), 0, can.x + int(can.w / 2), self.height())  # vert

                # draw horizontal and vertical prices
                # painter.setPen(QPen(cursor_color))
                # painter.setPen(QPen(cursor_color))
                # painter.setFont(QFont("arial"))
                # painter.drawText(QRectF(0, can.y + add_height, self.width(), 50), Qt.AlignRight, "test")

    def calc_y2(self, candle: Candle) -> float:
        percent_of_screen = (candle.low - self.global_min) / (self.global_max - self.global_min)
        pixel_height = percent_of_screen * self.height()
        distance_from_top = self.height() - pixel_height
        return distance_from_top

    def calc_y1(self, candle: Candle) -> float:
        percent_of_screen = (candle.high - self.global_min) / (self.global_max - self.global_min)
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

