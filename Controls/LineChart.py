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
from PyQt5 import QtWidgets, QtCore


class LineChart(Panel):
    def __init__(self, data: list[float], rgba: RGBA):
        super().__init__()
        if len(data) == 0:
            raise ValueError("Cannot have empty dataset")
        self.dataset = DataSet(data, rgba)
        self.min_datapoints_on_screen = 2
        self.max_datapoints_on_screen = 300
        self.last_index = len(data) - 1
        self.first_index = self.last_index - 2
        self.mouse_prev_x = None
        self.mouse_click_index = 0
        self.__mouse_x = 0
        self.__mouse_y = 0
        self.min_value_on_screen = 0
        self.max_value_on_screen = 0
        self.recalc_min_and_max()
        self.y_axis_width = 80
        self.x_axis_height = 40
        self.draw_x_axis = False
        self.draw_y_axis = False
        self.change_first_index_event = None
        self.change_last_index_event = None
        self.mouse_draw_event = None
        self.num_horizontal_gridlines = 8
        self.gridline_datapoints: list[int] = []
        self.__draw_gridlines = True
        self.__draw__vertical_cursor = True
        self.__draw__horizontal_cursor = True
        self.mouse_enter_event = None
        self.mouse_leave_event = None
        self._x_axis_labels: list[str] = None

    def set_x_axis_labels(self, labels: list[str]):
        self._x_axis_labels = labels

    @overrides
    def enterEvent(self, a0: QtCore.QEvent) -> None:
        super().enterEvent(a0)
        self.set_draw_vertical_cursor(True)
        self.set_draw_horizontal_cursor(True)
        if self.mouse_enter_event is not None:
            self.mouse_enter_event()

    @overrides
    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        super(LineChart, self).leaveEvent(a0)
        self.set_draw_vertical_cursor(False)
        self.set_draw_horizontal_cursor(False)
        if self.mouse_leave_event is not None:
            self.mouse_leave_event()

    def set_draw_vertical_cursor(self, draw: bool):
        self.__draw__vertical_cursor = draw

    def set_draw_horizontal_cursor(self, draw: bool):
        self.__draw__horizontal_cursor = draw

    def set_mouse_x(self, x: int):
        self.__mouse_x = x
        self.update()

    def set_draw_gridlines(self, draw: bool):
        self.__draw_gridlines = draw

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
        self.recalc_gridline_indexes()

        if self.change_first_index_event is not None:
            self.change_first_index_event(increment)

    def change_last_index(self, increment: bool):
        if increment:
            self.last_index += 1
        else:
            self.last_index -= 1
        self.recalc_min_and_max()
        self.recalc_min_and_max()
        self.recalc_gridline_indexes()

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
                self.recalc_gridline_indexes()

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

        self.__mouse_x = a0.x()
        self.__mouse_y = a0.y()

        self.update()

    def draw_mouse_cursor(self):
        if self.__draw__vertical_cursor:
            self.draw_vertical_mouse_line(self.__mouse_x)
        if self.__draw__horizontal_cursor:
            self.draw_horizontal_mouse_line(self.__mouse_y)

    def draw_horizontal_mouse_line(self, y: int):
        if self.__mouse_x > self.chart_width() or self.__mouse_y > self.chart_height():
            return
        self.painter.setPen(QPen(StyleInfo.color_cursor, StyleInfo.pen_width, Qt.DashLine))
        # draw horizontal line
        x1 = 0
        x2 = self.chart_width()
        self.painter.drawLine(x1, y, x2, y)
        if self.mouse_draw_event is not None:
            self.mouse_draw_event(self.__mouse_x, self.__mouse_y)
        self.update()

    def draw_vertical_mouse_line(self, x: int):
        if self.__mouse_x > self.chart_width() or self.__mouse_y > self.chart_height():
            return
        self.painter.setPen(QPen(StyleInfo.color_cursor, StyleInfo.pen_width, Qt.DashLine))

        y1 = 0
        y2 = self.chart_height()
        self.painter.drawLine(x, y1, x, y2)
        if self.mouse_draw_event is not None:
            self.mouse_draw_event(self.__mouse_x, self.__mouse_y)
        self.update()

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

    def draw_axis_labels(self):
        self.painter.setPen(QPen(QColor(255, 255, 255), .05, Qt.SolidLine))

    def recalc_gridline_indexes(self):
        if self.__draw_gridlines:
            self.gridline_datapoints = []
            if self.num_datapoints_on_screen() < 50:
                dist_between_indexes = int(self.num_datapoints_on_screen() / 4)
            else:
                dist_between_indexes = int(self.num_datapoints_on_screen() / 8)
            if dist_between_indexes != 0:
                for i in range(self.dataset.collection_length()):
                    if i % dist_between_indexes == 0:
                        self.gridline_datapoints.append(i)

    def draw_vertical_gridlines(self):
        if self.__draw_gridlines:
            self.painter.setPen(QPen(StyleInfo.color_grid_line, StyleInfo.gridline_width, Qt.SolidLine))
            for index in self.gridline_datapoints:
                if self.first_index < index < self.last_index:
                    x = self.get_x_for_datapoint(index)
                    self.painter.drawLine(x, 0, x, self.chart_height())

                    # find x axis value
                    self.painter.setPen(QPen(QColor(255, 255, 255), .05, Qt.SolidLine))
                    display_val = self.format_text_for_x_axis(index)
                    label_width = 100
                    self.painter.drawText(QRectF(x - int(label_width / 2),
                                                 self.chart_height(),
                                                 label_width,
                                                 self.x_axis_height), Qt.AlignHCenter | Qt.AlignCenter, display_val)

    def format_text_for_x_axis(self, index: int) -> str:
        if self._x_axis_labels is not None:
            return self._x_axis_labels[index]
        return str(index)

    def format_text_for_y_axis(self, text: float) -> str:
        return str(round(text, 2))  # override to change the format for the y axis labels

    def convert_y_to_value(self, y: float):
        return self.min_value_on_screen + ((self.chart_height() - y) / self.chart_height() * (self.max_value_on_screen - self.min_value_on_screen))

    def draw_y_axis_label(self, y: int):
        self.painter.setPen(QPen(QColor(255, 255, 255), .05, Qt.SolidLine))
        val = self.convert_y_to_value(y)
        label_height = 50
        self.painter.drawText(QRectF(self.chart_width(), y - label_height / 2, self.y_axis_width, label_height),
                              Qt.AlignHCenter | Qt.AlignCenter,
                              self.format_text_for_y_axis(val))

    def draw_horizontal_gridlines(self):
        if self.__draw_gridlines:
            num_labels_on_y_axis = self.num_horizontal_gridlines
            for i in range(int(num_labels_on_y_axis)):
                x1 = 0
                x2 = self.chart_width()
                y1 = int(i * (self.chart_height() / num_labels_on_y_axis)) + int(
                    (self.chart_height() / num_labels_on_y_axis) / 2)
                y2 = y1
                self.painter.setPen(QPen(StyleInfo.color_grid_line, StyleInfo.gridline_width, Qt.SolidLine))
                self.painter.drawLine(x1, y1, x2, y2)
                self.draw_y_axis_label(y1)
            self.draw_y_axis_label(self.__mouse_y)


    def draw_collections(self):
        collection: Collection
        for collection in self.dataset.collections():
            if len(collection) > 0:
                for i in range(self.first_index, self.last_index - 1):
                    self.draw_datapoint(i, collection)

    @overrides
    def draw_objects(self):
        self.draw_horizontal_gridlines()
        self.draw_vertical_gridlines()
        self.draw_collections()
        self.draw_axis_labels()
        self.draw_mouse_cursor()
