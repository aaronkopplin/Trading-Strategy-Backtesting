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

        # row one
        self.row_one_panel = QWidget()
        self.layout.addWidget(self.row_one_panel)
        self.row_one_panel_layout = QHBoxLayout()
        self.row_one_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.row_one_panel.setLayout(self.row_one_panel_layout)
        self.row_one_panel.setFixedHeight(50)

        # row two
        self.row_two_panel = QWidget()
        self.layout.addWidget(self.row_two_panel)
        self.row_two_panel_layout = QHBoxLayout()
        self.row_two_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.row_two_panel.setLayout(self.row_two_panel_layout)
        self.row_two_panel.setFixedHeight(50)

        # begin time frame
        self.begin_timeframe = QDateTimeEdit()
        self.begin_timeframe.setDateTime(QDateTime(date.today() - timedelta(7)))
        self.row_two_panel_layout.addWidget(self.begin_timeframe)

        # end time frame
        self.end_timeframe = QDateTimeEdit()
        self.end_timeframe.setDateTime(QDateTime(date.today()))
        self.row_two_panel_layout.addWidget(self.end_timeframe)

        #  candle selector
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
        self.row_two_panel_layout.addWidget(self.candle_selector)

        # submit_button button
        self.submit_button = QPushButton("submit")
        self.submit_button.clicked.connect(self.run_query)
        self.row_two_panel_layout.addWidget(self.submit_button)

    def run_query(self):
        self.chart.run_query(self.begin_timeframe.dateTime(),
                             self.end_timeframe.dateTime(),
                             self.candle_selector.currentText())


class Chart(QtWidgets.QWidget):
    def __init__(self, candles: list):
        super().__init__()
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

    def min_zoom(self) -> int:
        return int(float(len(self.candles)) / float(10))

    def num_candles_on_screen(self):
        return self.last_candle - self.first_candle

    def run_query(self, begin: QDateTime, end: QDateTime, interval: str):
        data = yfinance.download(["BTC-USD"],
                                 start=f"{begin.date().year()}-{begin.date().month()}-{begin.date().day()}",
                                 end=f"{end.date().year()}-{end.date().month()}-{end.date().day()}",
                                 interval=interval)
        data.to_csv("data.csv")
        self.candles = read_candles()
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

        # draw candle bodies
        self.candle_width = self.width() / self.num_candles_on_screen()
        for i in range(self.num_candles_on_screen()):
            curr_candle = self.candles[i + self.first_candle]
            prev_candle = self.candles[i + self.first_candle - 1]

            # draw wicks
            painter.setPen(QPen(Qt.black))
            x1 = (i * self.candle_width) + (self.candle_width / 2)
            y1 = self.calc_y1(curr_candle)
            x2 = x1
            y2 = self.calc_y2(curr_candle)
            painter.drawLine(x1, y1, x2, y2)

            # draw candle bodies
            if curr_candle.close >= curr_candle.open:
                painter.setPen(QPen(Qt.darkGreen, 1, Qt.SolidLine))
                painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            else:
                painter.setPen(QPen(Qt.darkRed, 1, Qt.SolidLine))
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))

            x = i * self.candle_width
            y = self.calc_y(curr_candle, self.global_max, self.global_min)
            w = self.candle_width
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
                x1 = ((i-1) * self.candle_width) + (self.candle_width / 2)
                y1 = self.convert_price_to_y(prev_candle.upper_band)
                x2 = (i * self.candle_width) + (self.candle_width / 2)
                y2 = self.convert_price_to_y(curr_candle.upper_band)
                if prev_candle.upper_band != 0 and curr_candle.upper_band != 0:
                    painter.drawLine(QLine(int(x1), y1, int(x2), y2))

                # simple moving average
                painter.setPen(QPen(Qt.darkMagenta))
                x1 = ((i - 1) * self.candle_width) + (self.candle_width / 2)
                y1 = self.convert_price_to_y(prev_candle.sma)
                x2 = (i * self.candle_width) + (self.candle_width / 2)
                y2 = self.convert_price_to_y(curr_candle.sma)
                if prev_candle.sma != 0 and curr_candle.sma != 0:
                    painter.drawLine(QLine(int(x1), y1, int(x2), y2))

                # lower band
                painter.setPen(QPen(Qt.darkCyan))
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
                painter.setPen(QPen(Qt.black))
                painter.setFont(QFont("arial"))
                price = f"Open: ${'{:,.2f}'.format(can.open)}\n" \
                        f"High: ${'{:,.2f}'.format(can.high)}\n" \
                        f"Low: ${'{:,.2f}'.format(can.low)}\n" \
                        f"Close: ${'{:,.2f}'.format(can.close)}"
                painter.drawText(QRectF(5, 5, self.width(), self.height()),
                                 Qt.AlignLeft|Qt.AlignTop,
                                 price + "\nDate: " + str(can_date))

                # draw cursor dashed lines
                painter.setPen(QPen(Qt.black, 1, Qt.DashLine))
                add_height = 0
                if not can.green():
                    add_height = can.h
                painter.drawLine(0, can.y + add_height, self.width(), can.y + add_height)  # horiz
                painter.drawLine(can.x + int(can.w / 2), 0, can.x + int(can.w / 2), self.height())  # vert

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

