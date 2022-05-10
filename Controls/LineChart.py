from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import StyleInfo
from Controls.Panel import Panel
from DataClasses.DataSet import DataSet
from DataClasses.RGBA import RGBA
from DataClasses.Collection import Collection
from overrides import overrides


def convert_price_to_str(price: float) -> str:
    return '${:,.0f}'.format(price)


class LineChart(Panel):
    def __init__(self, data: list[float], rgba: RGBA):
        super().__init__()
        if len(data) == 0:
            raise ValueError("Cannot have empty dataset")
        self.dataset = DataSet(data, rgba)
        self.min_datapoints_on_screen = 2
        self.max_datapoints_on_screen = 500
        self.last_index = len(data) - 1
        self.first_index = self.last_index - 2
        self.mouse_prev_x = None
        self.mouse_click_index = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.min_value_on_screen = 0
        self.max_value_on_screen = 0
        self.recalc_min_and_max()
        self.y_axis_width = 80
        self.x_axis_height = 50
        self.draw_x_axis = False
        self.draw_y_axis = False
        self.change_first_index_event = None
        self.change_last_index_event = None

    def set_draw_y_axis(self, draw: bool):
        self.draw_y_axis = draw
        self.update()

    def set_draw_x_axis(self, draw: bool):
        self.draw_x_axis = draw
        self.update()

    def chart_width(self):
        if self.draw_y_axis:
            return self.width() - self.y_axis_width
        else:
            return self.width()

    def chart_height(self):
        if self.draw_x_axis:
            return self.height() - self.x_axis_height
        else:
            return self.height()

    def min_zoom(self) -> int:
        collections = self.dataset.collections()
        lens = [len(collection) for collection in collections]
        return min(int(float(min(lens)) / float(10)), 10)

    def zoom_rate(self):
        val = int(self.num_datapoints_on_screen() * .1)
        if val == 0:
            val = 1
        if self.num_datapoints_on_screen() + val >= self.dataset.collection_length():
            val = self.dataset.collection_length() - self.num_datapoints_on_screen()
        return val

    def num_datapoints_on_screen(self):
        return self.last_index - self.first_index

    def recalc_min_and_max(self):
        self.min_value_on_screen = self.dataset.min_value_between_indexes(self.first_index, self.last_index)
        self.max_value_on_screen = self.dataset.max_value_between_indexes(self.first_index, self.last_index)
        self.update()

    def change_first_index(self, increment: bool):
        if increment:
            self.first_index += 1
        else:
            self.first_index -= 1
        self.recalc_min_and_max()
        if self.change_first_index_event is not None:
            self.change_first_index_event(increment)

    def change_last_index(self, increment: bool):
        if increment:
            self.last_index += 1
        else:
            self.last_index -= 1
        self.recalc_min_and_max()
        if self.change_last_index_event is not None:
            self.change_last_index_event(increment)

    @overrides
    def zoom_out(self):
        for i in range(self.zoom_rate()):
            if self.num_datapoints_on_screen() < self.dataset.collection_length() - 1 and self.num_datapoints_on_screen() < self.max_datapoints_on_screen:
                if self.first_index > 1:
                    self.change_first_index(False)
                if self.last_index < self.dataset.collection_length():
                    self.change_last_index(True)

    @overrides
    def zoom_in(self):
        for i in range(self.zoom_rate()):
            if self.num_datapoints_on_screen() > self.min_zoom():
                if self.first_index < self.last_index - self.min_zoom() - 1:
                    self.change_first_index(True)
                if self.last_index > 1:
                    self.change_last_index(False)

    def datapoint_width(self):
        num_points = self.last_index - self.first_index - 1
        return int(float(self.chart_width()) / float(num_points))

    def get_nearest_datapoint_index(self, x: int):
        return int(x / self.datapoint_width())

    @overrides
    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouse_prev_x = a0.x()
        self.mouse_click_index = self.get_nearest_datapoint_index(a0.x())
        super(LineChart, self).mousePressEvent(a0)

    def move_right(self, num_candles):
        while self.first_index > 0 and num_candles > 0:
            num_candles -= 1
            self.change_first_index(False)
            self.change_last_index(False)
        self.update()

    def move_left(self, num_candles):
        while self.last_index < self.dataset.collection_length() and num_candles > 0:
            num_candles -= 1
            self.change_first_index(True)
            self.change_last_index(True)
        self.update()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.mouse_down and self.handle_mouse_events:
            curr_index = self.get_nearest_datapoint_index(a0.x())
            if curr_index > self.mouse_click_index:
                self.move_right(curr_index - self.mouse_click_index)
                self.mouse_click_index = curr_index
            if curr_index < self.mouse_click_index:
                self.move_left(self.mouse_click_index - curr_index)
                self.mouse_click_index = curr_index

        self.mouse_x = a0.x()
        self.mouse_y = a0.y()
        self.update()

    def draw_mouse_cursor(self):
        if not self.mouse_entered:
            return
        self.painter.setPen(QPen(StyleInfo.color_cursor, StyleInfo.pen_width, Qt.DashLine))
        # draw horizontal line
        x1 = 0
        x2 = self.chart_width()
        y1 = self.mouse_y
        y2 = self.mouse_y
        self.painter.drawLine(x1, y1, x2, y2)

        # draw vertical line
        x1 = self.mouse_x
        x2 = self.mouse_x
        y1 = 0
        y2 = self.chart_height()
        self.painter.drawLine(x1, y1, x2, y2)

    def add_collection(self, data: list[float], rgb: RGBA):
        self.dataset.add_collection(data, rgb)
        self.update()

    def get_y_for_datapoint(self, item: float) -> int:
        height = item - self.min_value_on_screen
        delta = self.max_value_on_screen - self.min_value_on_screen
        if delta != 0:
            return int((height / delta) * self.chart_height())
        else:
            return int(self.height() / 2)

    def get_x_for_datapoint(self, i: int):
        length = (self.last_index - self.first_index) - 1
        index_on_screen = i - self.first_index
        return int((index_on_screen / length) * self.chart_width()) - int(self.datapoint_width() / 2.0)

    def draw_datapoint(self, i: int, collection: Collection):
        self.painter.setPen(QPen(collection.color.color(), StyleInfo.pen_width, Qt.SolidLine))
        first = collection[i]
        second = collection[i + 1]

        x1 = self.get_x_for_datapoint(i)
        y1 = self.get_y_for_datapoint(first)
        x2 = self.get_x_for_datapoint(i + 1)
        y2 = self.get_y_for_datapoint(second)
        self.painter.drawLine(x1, y1, x2, y2)

    @overrides
    def draw_objects(self):
        collection: Collection
        for collection in self.dataset.collections():
            if len(collection) > 0:
                for i in range(self.first_index, self.last_index - 1):
                    self.draw_datapoint(i, collection)
                    self.draw_mouse_cursor()
