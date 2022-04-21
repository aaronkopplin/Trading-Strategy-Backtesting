from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import  QBrush, QPen, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Candle import Candle
from PullData import read_candles
from Strategy import Account, Trade
import StyleInfo
import datetime
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import StyleInfo
from Controls.Panel import Panel


def convert_price_to_str(price: float) -> str:
    return '${:,.0f}'.format(price)


class LineChart(Panel):
    def __init__(self, data: list):
        super().__init__()
        self.y_axis_width = 100
        self.x_axis_height = 30
        self.data = data
        self.last_index = len(self.data)
        self.first_index = self.last_index - self.min_zoom()
        self.draw_boll_bands = False
        self.global_min = self.min_value()
        self.global_max = self.max_value()
        self.candle_bodies = []
        self.setMouseTracking(True)
        self.draw_cursor = True
        self.mouse_x = 0
        self.mouse_y = 0
        self.datapoint_width = self.chart_width() / self.num_datapoints_on_screen()
        self.mouse_prev_location = 0
        self.mouse_down = False
        self.draw_gridlines = True
        self.strategy_data_visible = True
        self.draw_trend_indicators = False
        self.num_labels_on_y_axis = 10
        self.num_vertical_gridlines = 10
        self.gridline_datapoints: list[int] = []
        self.compute_vertical_gridlines()

    def chart_width(self) -> int:
        return self.width() - self.y_axis_width

    def chart_height(self) -> int:
        return self.height() - self.x_axis_height

    def draw_bollinger_bands(self, visible: bool):
        self.draw_boll_bands = visible
        self.update()

    def trend_indicator_check_checkchanged(self, visible: bool):
        self.draw_trend_indicators = visible
        self.update()

    def clear(self):
        self.strategy_data_visible = False
        self.update()

    def strategy_run_event(self, account: Account):
        trade: Trade

        self.strategy_data_visible = True
        for trade in account.trades:
            buy_can: Candle = self.data[trade.buy_candle_index]
            buy_can.bought = True
            if trade.sell_candle_index:
                sell_can = self.data[trade.sell_candle_index]
                sell_can.sold = True
        self.update()

    def min_zoom(self) -> int:
        return min(int(float(len(self.data)) / float(10)), 10)

    def zoom_rate(self) -> int:
        return int(self.num_datapoints_on_screen() / 10)

    def num_datapoints_on_screen(self):
        return self.last_index - self.first_index

    def refresh_data(self):
        self.data = read_candles()
        self.last_index = len(self.data)
        self.first_index = self.last_index - self.min_zoom()
        self.update()

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouse_prev_location = a0.x()
        self.mouse_down = True

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouse_down = False

    def move_left(self, num_candles: int):
        while self.first_index > 0 and self.num_datapoints_on_screen() >= self.min_zoom() and num_candles > 0:
            self.last_index -= 1
            self.first_index -= 1
            num_candles -= 1
        self.update()

    def move_right(self, num_candles: int):
        while self.last_index < len(
                self.data) and self.num_datapoints_on_screen() >= self.min_zoom() and num_candles > 0:
            self.first_index += 1
            self.last_index += 1
            num_candles -= 1
        self.update()

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.draw_cursor = True

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.draw_cursor = False
        self.update()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.mouse_down:
            if a0.x() > self.mouse_prev_location + self.datapoint_width:
                distance = a0.x() - self.mouse_prev_location
                num_candles = distance / self.datapoint_width
                self.move_left(int(num_candles))
                self.mouse_prev_location = a0.x()
            if a0.x() < self.mouse_prev_location - self.datapoint_width:
                distance = self.mouse_prev_location - a0.x()
                num_candles = distance / self.datapoint_width
                self.mouse_prev_location = a0.x()
                self.move_right(int(num_candles))
        self.mouse_x = a0.x()
        self.mouse_y = a0.y()
        self.update()

    def zoom_out(self):
        for i in range(self.zoom_rate()):
            if self.num_datapoints_on_screen() < len(self.data) - 1:
                if self.first_index > 1:
                    self.first_index -= 1
                if self.last_index < len(self.data):
                    self.last_index += 1

    def zoom_in(self):
        for i in range(self.zoom_rate()):
            if self.num_datapoints_on_screen() > self.min_zoom():
                if self.first_index < self.last_index - self.min_zoom() - 1:
                    self.first_index += 1
                if self.last_index > 1:
                    self.last_index -= 1

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        if a0.angleDelta().y() < 0:  # zoom out
            self.zoom_out()

        if a0.angleDelta().y() > 0:  # zoom in
            self.zoom_in()
        self.compute_vertical_gridlines()
        self.update()

    def compute_vertical_gridlines(self):
        # compute which candles are vertical gridline candles
        self.gridline_datapoints = []
        for i in range(len(self.data)):
            dist_between_gridline_candles = int(self.num_datapoints_on_screen() / self.num_vertical_gridlines)
            if i % dist_between_gridline_candles == 0:
                self.gridline_datapoints.append(i)

    def find_candle(self, x: float) -> Candle:
        for can in self.candle_bodies:
            if can.x <= x <= (can.x + can.w):
                return can

    def convert_y_to_price(self, y: int) -> float:
        return self.global_min + ((self.chart_height() - y) / self.chart_height() * (self.global_max - self.global_min))

    def convert_price_to_y(self, price: float) -> int:
        return self.chart_height() - int(
            ((price - self.global_min) / (self.global_max - self.global_min)) * self.chart_height())

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_objects(painter)
        painter.end()

    def min_value(self):
        cans = self.data[self.first_index:self.last_index]
        lows = [can.low for can in cans if can.low != 0]
        if self.draw_boll_bands:
            lower_bands = [can.lower_band for can in cans if can.lower_band != 0]
            return min(lows + lower_bands)
        return min(lows)

    def max_value(self):
        cans = self.data[self.first_index:self.last_index]
        highs = [can.high for can in cans if can.high != 0]
        if self.draw_boll_bands:
            upper_bands = [can.upper_band for can in cans if can.upper_band != 0]
            return max(highs + upper_bands)
        return max(highs)

    def draw_vertical_gridlines(self, painter: QPainter, index: int):
        if not self.draw_gridlines:
            return
        # draw grid lines
        if index + self.first_index in self.gridline_datapoints:
            painter.setPen(QPen(StyleInfo.color_grid_line, StyleInfo.pen_width, Qt.SolidLine))
            x = self.__get_x_for_candle_index(index)
            painter.drawLine(x, 0, x, self.chart_height())
            self.__draw_dates_for_vertical_gridlines(painter, index)

    def draw_background(self, painter):
        #  draw background
        painter.setPen(QPen(StyleInfo.color_background, StyleInfo.pen_width, Qt.SolidLine))
        painter.setBrush(QBrush(StyleInfo.color_background, Qt.SolidPattern))
        painter.drawRect(0, 0, self.chart_width(), self.chart_height())

        # returns the x value for the middle of the candle

    def __get_x_for_candle_index(self, index: int) -> int:
        return int((index * self.datapoint_width) + (self.datapoint_width / 2))

    def draw_candle_wicks(self, painter: QPainter, curr_candle: Candle, index: int):
        # draw wicks
        x = self.__get_x_for_candle_index(index)
        y1 = int(self.calc_y1(curr_candle))
        y2 = int(self.calc_y2(curr_candle))
        if curr_candle.close >= curr_candle.open:
            painter.setPen(QPen(StyleInfo.color_green_candle, StyleInfo.pen_width, Qt.SolidLine))
        else:
            painter.setPen(QPen(StyleInfo.color_red_candle, StyleInfo.pen_width, Qt.SolidLine))
        painter.drawLine(x, y1, x, y2)

    def get_dimensions_for_curr_candle(self, curr_candle: Candle, index: int):
        # dimensions for candle bodies
        x = int(index * self.datapoint_width)
        y = int(self.calc_y(curr_candle, self.global_max, self.global_min))
        w = int(self.datapoint_width)
        h = int(self.calc_candle_height(curr_candle, self.global_max, self.global_min))
        return x, y, w, h

    def draw_strategy_indicators(self, painter: QPainter, curr_candle: Candle, x, y, w, h):
        if self.strategy_data_visible:
            self.draw_sell_indicator(painter, curr_candle, x, y, w, h)
            self.draw_buy_indicator(painter, curr_candle, x, y, w, h)

    def draw_buy_sell_indicators(self, painter: QPainter, curr_candle: Candle, x: int, w: int):
        # if strategy has run and candle is bought or sold
        if self.strategy_data_visible:
            if curr_candle.bought:
                painter.setPen(QPen(StyleInfo.color_strategy_buy, 0, Qt.NoPen))  # get rid of edges
                painter.setBrush(QBrush(StyleInfo.color_strategy_buy, Qt.SolidPattern))
                painter.drawRect(x, 0, w, self.chart_height())
            if curr_candle.sold:
                painter.setPen(QPen(QColor(0, 0, 0, 0), 0, Qt.NoPen))  # get rid of edges
                painter.setBrush(QBrush(StyleInfo.color_strategy_sell, Qt.SolidPattern))
                painter.drawRect(x, 0, w, self.chart_height())

    def __draw_triangle(self, x: int, y: int, w: int, h: int, painter: QPainter, color: QColor):
        rect = QRectF(x, y, w, h)
        path = QPainterPath()
        path.moveTo(rect.left() + (rect.width() / 2), rect.top())
        path.lineTo(rect.bottomLeft())
        path.lineTo(rect.bottomRight())
        path.lineTo(rect.left() + (rect.width() / 2), rect.top())
        painter.fillPath(path, QBrush(color))

    def draw_cursor_and_price_info(self, painter: QPainter):
        if self.draw_cursor:
            #  draw price, datetime next to cursor
            can = self.find_candle(self.mouse_x)
            if can is not None:
                can_date = can.date_time
                painter.setPen(QPen(Qt.white))
                # painter.setFont(QFont("arial", StyleInfo.font_size))
                price = f"Open: ${'{:,.2f}'.format(can.open)}, " \
                        f"High: ${'{:,.2f}'.format(can.high)}, " \
                        f"Low: ${'{:,.2f}'.format(can.low)}, " \
                        f"Close: ${'{:,.2f}'.format(can.close)}, "
                can_date = "Date: " + str(can_date)
                painter.drawText(QRectF(5, 5, self.chart_width(), self.chart_height()),
                                 Qt.AlignLeft | Qt.AlignTop,
                                 price + can_date)

                # draw cursor dashed lines
                painter.setPen(QPen(StyleInfo.color_cursor, StyleInfo.pen_width, Qt.DashLine))
                add_height = 0
                if not can.green():
                    add_height = can.h
                painter.drawLine(0, can.y + add_height, self.chart_width(), can.y + add_height)  # horiz
                painter.drawLine(can.x + int(can.w / 2), 0, can.x + int(can.w / 2), self.chart_height())  # vert

    def __draw_bollinger_bands(self, painter: QPainter, prev_candle: Candle, curr_candle: Candle, i: int):
        if i == 0: return
        if not self.draw_boll_bands: return

        # upper band
        painter.setPen(QPen(StyleInfo.color_bollinger_band, StyleInfo.pen_width, Qt.SolidLine))
        x1 = ((i - 1) * self.datapoint_width) + (self.datapoint_width / 2)
        y1 = self.convert_price_to_y(prev_candle.upper_band)
        x2 = (i * self.datapoint_width) + (self.datapoint_width / 2)
        y2 = self.convert_price_to_y(curr_candle.upper_band)
        if prev_candle.upper_band != 0 and curr_candle.upper_band != 0:
            painter.drawLine(QLine(int(x1), y1, int(x2), y2))

        # simple moving average
        painter.setPen(QPen(Qt.white, StyleInfo.pen_width, Qt.SolidLine))
        x1 = ((i - 1) * self.datapoint_width) + (self.datapoint_width / 2)
        y1 = self.convert_price_to_y(prev_candle.sma)
        x2 = (i * self.datapoint_width) + (self.datapoint_width / 2)
        y2 = self.convert_price_to_y(curr_candle.sma)
        if prev_candle.sma != 0 and curr_candle.sma != 0:
            painter.drawLine(QLine(int(x1), y1, int(x2), y2))

        # lower band
        painter.setPen(QPen(StyleInfo.color_bollinger_band, StyleInfo.pen_width, Qt.SolidLine))
        x1 = ((i - 1) * self.datapoint_width) + (self.datapoint_width / 2)
        y1 = self.convert_price_to_y(prev_candle.lower_band)
        x2 = (i * self.datapoint_width) + (self.datapoint_width / 2)
        y2 = self.convert_price_to_y(curr_candle.lower_band)
        if prev_candle.lower_band != 0 and curr_candle.lower_band != 0:
            painter.drawLine(QLine(int(x1), y1, int(x2), y2))

    def draw_sell_indicator(self, painter: QPainter, curr_candle: Candle, x, y, w, h):
        # draw horizontal line where sold
        if curr_candle.sell_price != 0:
            line_height = self.convert_price_to_y(curr_candle.sell_price)
            self.__draw_triangle(x, line_height, w, 20, painter, StyleInfo.color_red_candle)

    def draw_buy_indicator(self, painter: QPainter, curr_candle: Candle, x, y, w, h):
        # draw horizontal line where sold
        if curr_candle.bought_price != 0:
            line_height = self.convert_price_to_y(curr_candle.bought_price)
            self.__draw_triangle(x, line_height, w, 20, painter, StyleInfo.color_green_candle)

    def draw_candle_bodies(self, painter: QPainter, curr_candle: Candle, x, y, w, h):
        # draw candle bodies
        if curr_candle.green():
            painter.setPen(QPen(StyleInfo.color_green_candle, StyleInfo.pen_width, Qt.SolidLine))
            painter.setBrush(QBrush(StyleInfo.color_background, Qt.SolidPattern))
        else:
            painter.setPen(QPen(StyleInfo.color_red_candle, StyleInfo.pen_width, Qt.SolidLine))
            painter.setBrush(QBrush(StyleInfo.color_background, Qt.SolidPattern))

        painter.drawRect(x, y, w, h)
        curr_candle.x = x
        curr_candle.y = y
        curr_candle.w = w
        curr_candle.h = h
        self.candle_bodies.append(curr_candle)

    def calc_y2(self, candle: Candle) -> float:
        percent_of_screen = (candle.low - self.global_min) / (self.global_max - self.global_min)
        pixel_height = percent_of_screen * self.chart_height()
        distance_from_top = self.chart_height() - pixel_height
        return distance_from_top

    def calc_y1(self, candle: Candle) -> float:
        percent_of_screen = (candle.high - self.global_min) / (self.global_max - self.global_min)
        pixel_height = percent_of_screen * self.chart_height()
        distance_from_top = self.chart_height() - pixel_height
        return distance_from_top

    def calc_y(self, candle: Candle, global_max: float, global_min: float) -> float:
        candle_top = max(candle.open, candle.close)
        percent_of_screen = (candle_top - global_min) / (global_max - global_min)
        pixel_height = percent_of_screen * self.chart_height()
        distance_from_top = self.chart_height() - pixel_height
        return distance_from_top

    def calc_candle_height(self, candle: Candle, global_max: float, global_min: float) -> float:
        h = max(candle.open, candle.close) - min(candle.open, candle.close)
        distance = global_max - global_min
        percent = h / distance
        return percent * self.chart_height()

    def __draw_price_gutter_prices(self, painter: QPainter):
        for i in range(self.num_labels_on_y_axis):
            x = self.chart_width()
            y = int(i * (self.chart_height() / self.num_labels_on_y_axis))
            w = self.y_axis_width
            h = int((self.chart_height() / self.num_labels_on_y_axis))
            price = self.convert_y_to_price(int(y + (h / 2)))
            painter.setPen(QPen(Qt.white, StyleInfo.pen_width, Qt.SolidLine))
            painter.drawText(QRectF(x, y, w, h),
                             Qt.AlignHCenter | Qt.AlignCenter,
                             convert_price_to_str(price))

    def __draw_dates_for_vertical_gridlines(self, painter: QPainter, index: int):
        painter.setPen(QPen(Qt.white, StyleInfo.pen_width, Qt.SolidLine))
        can: Candle = self.data[index + self.first_index]
        date_time = datetime.datetime.strptime(can.date_time[:len(can.date_time) - 6], '%Y-%m-%d %H:%M:%S').strftime(
            '%d %H:%M')
        w = 100
        x = self.__get_x_for_candle_index(index)
        painter.drawText(QRectF(x - int(w / 2),
                                self.chart_height(),
                                w,
                                self.x_axis_height),
                         Qt.AlignHCenter | Qt.AlignCenter,
                         date_time)

    def draw_horizontal_gridlines(self, painter: QPainter):
        if not self.draw_gridlines:
            return
        #  draw horizontal gridlines
        painter.setPen(QPen(StyleInfo.color_grid_line, StyleInfo.pen_width, Qt.SolidLine))
        for i in range(self.num_labels_on_y_axis):
            x1 = 0
            x2 = self.chart_width()
            y1 = int(i * (self.chart_height() / self.num_labels_on_y_axis)) + int(
                (self.chart_height() / self.num_labels_on_y_axis) / 2)
            y2 = y1
            painter.drawLine(x1, y1, x2, y2)

    def draw_objects(self, painter: QPainter):
        self.global_min = self.min_value()
        self.global_max = self.max_value()
        self.candle_bodies.clear()
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        self.draw_background(painter)
        self.draw_horizontal_gridlines(painter)

        # draw candle bodies
        self.datapoint_width = self.chart_width() / self.num_datapoints_on_screen()
        for i in range(self.num_datapoints_on_screen()):
            curr_candle: Candle = self.data[i + self.first_index]
            prev_candle: Candle = self.data[i + self.first_index - 1]
            self.draw_vertical_gridlines(painter, i)
            self.draw_candle_wicks(painter, curr_candle, i)
            x, y, w, h = self.get_dimensions_for_curr_candle(curr_candle, i)
            self.draw_candle_bodies(painter, curr_candle, x, y, w, h)
            self.draw_strategy_indicators(painter, curr_candle, x, y, w, h)
            self.__draw_bollinger_bands(painter, prev_candle, curr_candle, i)

        self.draw_cursor_and_price_info(painter)
        self.__draw_price_gutter_prices(painter)



