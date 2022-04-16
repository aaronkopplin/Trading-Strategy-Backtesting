from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import  QBrush, QPen, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Candle import Candle
import yfinance
from PullData import read_candles
from Strategy import Account, Trade
import StyleInfo


def convert_price_to_str(price: float) -> str:
    return '${:,.0f}'.format(price)


class CandleChart(QtWidgets.QWidget):
    def __init__(self, candles: list):
        super().__init__()
        self.price_gutter_width = 100
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
        self.candle_width = self.__candle_chart_width() / self.num_candles_on_screen()
        self.mouse_prev_location = 0
        self.mouse_down = False
        self.draw_gridlines = True
        self.strategy_data_visible = True
        self.draw_boll_bands = False
        self.draw_trend_indicators = False
        self.num_prices_in_gutter = 10
        self.num_vertical_gridlines = 10

    def __candle_chart_width(self) -> int:
        return self.width() - self.price_gutter_width

    def draw_bollinger_bands(self, visible: bool):
        self.draw_boll_bands = visible
        self.update()

    def trend_indicator_check_checkchanged(self, visible: bool):
        self.draw_trend_indicators = visible
        self.update()

    def __clear(self):
        self.strategy_data_visible = False
        self.update()

    def strategy_run_event(self, account: Account):
        trade: Trade

        self.strategy_data_visible = True
        for trade in account.trades:
            buy_can: Candle = self.candles[trade.buy_candle_index]
            buy_can.bought = True
            if trade.sell_candle_index:
                sell_can = self.candles[trade.sell_candle_index]
                sell_can.sold = True
        self.update()

    def min_zoom(self) -> int:
        return min(int(float(len(self.candles)) / float(10)), 10)

    def zoom_rate(self) -> int:
        return int(self.num_candles_on_screen() / 10)

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
            for i in range(self.zoom_rate()):
                if self.num_candles_on_screen() < len(self.candles) - 1:
                    if self.first_candle > 1:
                        self.first_candle -= 1
                    if self.last_candle < len(self.candles):
                        self.last_candle += 1
                    # elif self.last_candle < len(self.candles):
                    #     self.last_candle += 1

        if a0.angleDelta().y() > 0:  # zoom in
            for i in range(self.zoom_rate()):
                if self.num_candles_on_screen() > self.min_zoom():
                    if self.first_candle < self.last_candle - self.min_zoom() - 1:
                        self.first_candle += 1
                    if self.last_candle > 1:
                        self.last_candle -= 1
                    # elif self.last_candle > self.first_candle + self.min_zoom():
                    #     self.last_candle -= 1

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

    def draw_vertical_gridlines(self, painter: QPainter, index: int, x1: int):
        if not self.draw_gridlines:
            return
        # draw grid lines
        if (index + int(self.num_candles_on_screen() / (2 * self.num_vertical_gridlines))) % int(self.num_candles_on_screen() / self.num_vertical_gridlines) == 0:
            painter.setPen(QPen(StyleInfo.color_grid_line, StyleInfo.pen_width, Qt.SolidLine))
            painter.drawLine(x1, 0, x1, self.height())

    def draw_background(self, painter):
        #  draw background
        painter.setPen(QPen(StyleInfo.color_background, StyleInfo.pen_width, Qt.SolidLine))
        painter.setBrush(QBrush(StyleInfo.color_background, Qt.SolidPattern))
        painter.drawRect(0, 0, self.__candle_chart_width(), self.height())

    def __get_x_for_candle_index(self, index: int) -> int:
        return int((index * self.candle_width) + (self.candle_width / 2))

    def draw_candle_wicks(self, painter: QPainter, curr_candle: Candle, index: int):
        # draw wicks
        x1 = self.__get_x_for_candle_index(index)
        y1 = int(self.calc_y1(curr_candle))
        x2 = int(x1)
        y2 = int(self.calc_y2(curr_candle))
        if curr_candle.close >= curr_candle.open:
            painter.setPen(QPen(StyleInfo.color_green_candle, StyleInfo.pen_width, Qt.SolidLine))
        else:
            painter.setPen(QPen(StyleInfo.color_red_candle, StyleInfo.pen_width, Qt.SolidLine))
        painter.drawLine(x1, y1, x2, y2)
        return x1, y1, x2, y2

    def get_dimensions_for_curr_candle(self, curr_candle: Candle, index: int):
        # dimensions for candle bodies
        x = int(index * self.candle_width)
        y = int(self.calc_y(curr_candle, self.global_max, self.global_min))
        w = int(self.candle_width)
        h = int(self.calc_candle_height(curr_candle, self.global_max, self.global_min))
        return x, y, w, h

    def draw_buy_sell_indicators(self, painter: QPainter, curr_candle: Candle, x: int, w: int):
        # if strategy has run and candle is bought or sold
        if self.strategy_data_visible:
            if curr_candle.bought:
                painter.setPen(QPen(QColor(0, 0, 0, 0), 0, Qt.SolidLine))  # get rid of edges
                painter.setBrush(QBrush(StyleInfo.color_strategy_buy, Qt.SolidPattern))
                painter.drawRect(x, 0, w, self.height())
            if curr_candle.sold:
                painter.setPen(QPen(QColor(0, 0, 0, 0), 0, Qt.SolidLine))  # get rid of edges
                painter.setBrush(QBrush(StyleInfo.color_strategy_sell, Qt.SolidPattern))
                painter.drawRect(x, 0, w, self.height())

    def __draw_triangle(self, x: int, y: int, w: int, h: int, painter: QPainter):
        rect = QRectF(x, y, w, h)
        path = QPainterPath()
        path.moveTo(rect.left() + (rect.width() / 2), rect.top())
        path.lineTo(rect.bottomLeft())
        path.lineTo(rect.bottomRight())
        path.lineTo(rect.left() + (rect.width() / 2), rect.top())
        painter.fillPath(path, QBrush(QColor("blue")))

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
                painter.drawText(QRectF(5, 5, self.__candle_chart_width(), self.height()),
                                 Qt.AlignLeft|Qt.AlignTop,
                                 price + can_date)

                # draw cursor dashed lines
                painter.setPen(QPen(StyleInfo.color_cursor, StyleInfo.pen_width, Qt.DashLine))
                add_height = 0
                if not can.green():
                    add_height = can.h
                painter.drawLine(0, can.y + add_height, self.__candle_chart_width(), can.y + add_height)  # horiz
                painter.drawLine(can.x + int(can.w / 2), 0, can.x + int(can.w / 2), self.height())  # vert

    def __draw_bollinger_bands(self, painter: QPainter, prev_candle: Candle, curr_candle: Candle, i: int):
        if i == 0: return
        if not self.draw_boll_bands: return

        # upper band
        painter.setPen(QPen(StyleInfo.color_bollinger_band, StyleInfo.pen_width, Qt.SolidLine))
        x1 = ((i - 1) * self.candle_width) + (self.candle_width / 2)
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
        painter.setPen(QPen(StyleInfo.color_bollinger_band, StyleInfo.pen_width, Qt.SolidLine))
        x1 = ((i - 1) * self.candle_width) + (self.candle_width / 2)
        y1 = self.convert_price_to_y(prev_candle.lower_band)
        x2 = (i * self.candle_width) + (self.candle_width / 2)
        y2 = self.convert_price_to_y(curr_candle.lower_band)
        if prev_candle.lower_band != 0 and curr_candle.lower_band != 0:
            painter.drawLine(QLine(int(x1), y1, int(x2), y2))

    def draw_sell_indicator(self, painter: QPainter, curr_candle: Candle, x, y, w, h):
        # draw horizontal line where sold
        if curr_candle.sell_price != 0:
            line_height = self.convert_price_to_y(curr_candle.sell_price)
            self.__draw_triangle(x, line_height, w, 20, painter)

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

    def __draw_price_gutter_prices(self, painter: QPainter):
        for i in range(self.num_prices_in_gutter):
            x = self.__candle_chart_width()
            y = int(i * (self.height() / self.num_prices_in_gutter))
            w = self.price_gutter_width
            h = int((self.height() / self.num_prices_in_gutter))
            price = self.convert_y_to_price(int(y+(h/2)))
            painter.setPen(QPen(Qt.white, StyleInfo.pen_width, Qt.SolidLine))
            painter.drawText(QRectF(x,y,w,h),
                             Qt.AlignHCenter | Qt.AlignCenter,
                             convert_price_to_str(price))

    def draw_horizontal_gridlines(self, painter: QPainter):
        if not self.draw_gridlines:
            return
        #  draw horizontal gridlines
        painter.setPen(QPen(StyleInfo.color_grid_line, StyleInfo.pen_width, Qt.SolidLine))
        for i in range(self.num_prices_in_gutter):
            x1 = 0
            x2 = self.__candle_chart_width()
            y1 = int(i * (self.height() / self.num_prices_in_gutter)) + int((self.height() / self.num_prices_in_gutter) / 2)
            y2 = y1
            painter.drawLine(x1, y1, x2, y2)

    def draw_objects(self, painter: QPainter):
        self.global_min = self.min_candle_val()
        self.global_max = self.max_candle_val()
        self.candle_bodies.clear()
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        self.draw_background(painter)
        self.draw_horizontal_gridlines(painter)

        # draw candle bodies
        self.candle_width = self.__candle_chart_width() / self.num_candles_on_screen()
        for i in range(self.num_candles_on_screen()):
            curr_candle: Candle = self.candles[i + self.first_candle]
            prev_candle: Candle = self.candles[i + self.first_candle - 1]
            self.draw_vertical_gridlines(painter, i, self.__get_x_for_candle_index(i))
            x1, y1, x2, y2 = self.draw_candle_wicks(painter, curr_candle, i)
            x, y, w, h = self.get_dimensions_for_curr_candle(curr_candle, i)
            self.draw_buy_sell_indicators(painter, curr_candle, x, w)
            self.draw_candle_bodies(painter, curr_candle, x, y, w, h)
            self.draw_sell_indicator(painter, curr_candle, x, y, w, h)

            # draw bollinger bands
            self.__draw_bollinger_bands(painter, prev_candle, curr_candle, i)

        self.draw_cursor_and_price_info(painter)
        self.__draw_price_gutter_prices(painter)

