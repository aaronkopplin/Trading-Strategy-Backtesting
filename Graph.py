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


class Graph(QtWidgets.QWidget):
    def __init__(self, candles: list):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.chart = Chart(candles)
        self.layout.addWidget(self.chart)
        self.setLayout(self.layout)
        self.options_panel = QWidget()
        self.layout.addWidget(self.options_panel)
        self.options_layout = QGridLayout()
        self.options_layout.setContentsMargins(0, 0, 0, 0)
        self.options_panel.setLayout(self.options_layout)
        self.move_left = QPushButton("move left")
        self.move_left.clicked.connect(self.chart.move_left)
        self.move_right = QPushButton("move right")
        self.move_right.clicked.connect(self.chart.move_right)
        self.increase_candles = QPushButton("zoom out")
        self.increase_candles.clicked.connect(self.chart.increase_candles)
        self.decrease_candles = QPushButton("zoom in")
        self.decrease_candles.clicked.connect(self.chart.decrease_candles)
        self.options_layout.addWidget(self.move_left, 0, 0)
        self.options_layout.addWidget(self.move_right, 0, 1)
        self.options_layout.addWidget(self.increase_candles, 0, 2)
        self.options_layout.addWidget(self.decrease_candles, 0, 3)
        self.begin_timeframe = QDateTimeEdit()
        self.begin_timeframe.setDateTime(QDateTime(date.today() - timedelta(7)))
        self.end_timeframe = QDateTimeEdit()
        self.end_timeframe.setDateTime(QDateTime(date.today()))
        self.candle_selector = QComboBox()
        self.candle_selector.addItem("1m")
        self.candle_selector.addItem("2m")
        self.candle_selector.addItem("5m")
        self.candle_selector.addItem("15m")
        self.candle_selector.addItem("30m")
        self.candle_selector.addItem("1h")
        self.candle_selector.addItem("1d")
        self.candle_selector.addItem("5d")
        self.candle_selector.addItem("1wk")
        self.submit_button = QPushButton("submit")
        self.options_layout.addWidget(self.begin_timeframe, 1, 0)
        self.options_layout.addWidget(self.end_timeframe, 1, 1)
        self.options_layout.addWidget(self.candle_selector, 1, 2)
        self.options_layout.addWidget(self.submit_button, 1, 3)
        self.submit_button.clicked.connect(self.run_query)
        self.options_panel.setFixedHeight(100)

    def run_query(self):
        self.chart.run_query(self.begin_timeframe.dateTime(),
                             self.end_timeframe.dateTime(),
                             self.candle_selector.currentText())


class Chart(QtWidgets.QWidget):
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
        self.num_candles_on_screen = 20
        self.last_candle = len(self.candles)

    def run_query(self, begin: QDateTime, end: QDateTime, interval: str):
        data = yfinance.download(["BTC-USD"],
                                 start=f"{begin.date().year()}-{begin.date().month()}-{begin.date().day()}",
                                 end=f"{end.date().year()}-{end.date().month()}-{end.date().day()}",
                                 interval=interval)
        data.to_csv("data.csv")
        self.candles = read_candles()
        self.update()

    def move_left(self):
        if self.last_candle > 0:
            self.last_candle -= 1
            self.update()

    def move_right(self):
        if self.last_candle < len(self.candles):
            self.last_candle += 1
            self.update()

    def increase_candles(self):
        if self.num_candles_on_screen < len(self.candles):
            self.num_candles_on_screen += 1
            self.update()

    def decrease_candles(self):
        if self.num_candles_on_screen > 1:
            self.num_candles_on_screen -= 1
            self.update()

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
        for can in self.candle_bodies:
            # and y >= rect["y"] and y <= rect["y"] + rect["h"]
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

    def first_candle(self):
        return self.last_candle - self.num_candles_on_screen

    def draw_objects(self, painter: QPainter):
        self.global_min = min([can.lower_band for can in self.candles[self.first_candle():self.last_candle] if can.lower_band != 0])
        self.global_max = max([can.upper_band for can in self.candles[self.first_candle():self.last_candle] if can.upper_band != 0])
        self.candle_bodies.clear()
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        # draw candle bodies
        candle_width = self.width() / self.num_candles_on_screen
        for i in range(self.num_candles_on_screen):
            curr_candle = self.candles[i + self.first_candle()]
            prev_candle = self.candles[i + self.first_candle() - 1]

            # draw wicks
            painter.setPen(QPen(Qt.black))
            x1 = (i * candle_width) + (candle_width / 2)
            y1 = self.calc_y1(curr_candle, self.global_max, self.global_min)
            x2 = x1
            y2 = self.calc_y2(curr_candle, self.global_max, self.global_min)
            painter.drawLine(x1, y1, x2, y2)

            # draw candle bodies
            if curr_candle.close >= curr_candle.open:
                painter.setPen(QPen(Qt.darkGreen, 1, Qt.SolidLine))
                painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            else:
                painter.setPen(QPen(Qt.darkRed, 1, Qt.SolidLine))
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))

            x = i * candle_width
            y = self.calc_y(curr_candle, self.global_max, self.global_min)
            w = candle_width
            h = self.calc_candle_height(curr_candle, self.global_max, self.global_min)
            painter.drawRect(x, y, w, h)
            curr_candle.x = x
            curr_candle.y = y
            curr_candle.w = w
            curr_candle.h = h
            self.candle_bodies.append(curr_candle)

            # draw bollinger bands
            if i > 1:
                # upper band
                painter.setPen(QPen(Qt.blue))
                x1 = ((i-1) * candle_width) + (candle_width / 2)
                y1 = self.convert_price_to_y(prev_candle.upper_band)
                x2 = (i * candle_width) + (candle_width / 2)
                y2 = self.convert_price_to_y(curr_candle.upper_band)
                if prev_candle.upper_band != 0 and curr_candle.upper_band != 0:
                    painter.drawLine(QLine(int(x1), y1, int(x2), y2))

                # simple moving average
                painter.setPen(QPen(Qt.darkMagenta))
                x1 = ((i - 1) * candle_width) + (candle_width / 2)
                y1 = self.convert_price_to_y(prev_candle.sma)
                x2 = (i * candle_width) + (candle_width / 2)
                y2 = self.convert_price_to_y(curr_candle.sma)
                if prev_candle.sma != 0 and curr_candle.sma != 0:
                    painter.drawLine(QLine(int(x1), y1, int(x2), y2))

                # lower band
                painter.setPen(QPen(Qt.darkCyan))
                x1 = ((i - 1) * candle_width) + (candle_width / 2)
                y1 = self.convert_price_to_y(prev_candle.lower_band)
                x2 = (i * candle_width) + (candle_width / 2)
                y2 = self.convert_price_to_y(curr_candle.lower_band)
                if prev_candle.lower_band != 0 and curr_candle.lower_band != 0:
                    painter.drawLine(QLine(int(x1), y1, int(x2), y2))

        if self.draw_cursor:
            #  draw price, datetime next to cursor
            can = self.find_candle(self.mouse_x)
            if can is not None:
                can_date = can.date_time
                painter.setPen(QPen(Qt.black))
                painter.setFont(QFont("arial"))
                price = f"${'${:,.2f}'.format(can.open)}, " \
                        f"${'${:,.2f}'.format(can.high)}, " \
                        f"${'${:,.2f}'.format(can.low)}, " \
                        f"${'${:,.2f}'.format(can.close)}"
                add_height = 0
                if not can.green():
                    add_height = can.h
                painter.drawText(QPoint(int(can.x + int(can.w / 2)) + 5, int(can.y + add_height) - 5),
                                 price + ", " + str(can_date))

                # draw cursor dashed lines
                painter.setPen(QPen(Qt.black, 1, Qt.DashLine))
                add_height = 0
                if not can.green():
                    add_height = can.h
                painter.drawLine(0, can.y + add_height, self.width(), can.y + add_height)  # horiz
                painter.drawLine(can.x + int(can.w / 2), 0, can.x + int(can.w / 2), self.height())  # vert

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

