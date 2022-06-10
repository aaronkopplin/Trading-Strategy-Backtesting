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
from DataClasses.Label import Label
from overrides import overrides
from PyQt5 import QtWidgets, QtCore


class LineChart(Panel):
    def __init__(self, title: str, data: list[float], rgba: RGBA):
        super().__init__()
        if len(data) == 0:
            raise ValueError("Cannot have empty dataset")
        self.initial_data = (title, data, rgba)
        self.dataset: DataSet = None
        self.create_dataset(title, data, rgba)
        self.min_datapoints_on_screen = 2
        self.max_datapoints_on_screen = 300
        self.last_index = len(data)
        self.first_index = self.last_index - 1
        self.mouse_prev_x = None
        self.mouse_click_index = 0
        self._mouse_x = 0
        self._mouse_y = 0
        self.min_value_on_screen = 0
        self.max_value_on_screen = 0
        self.recalc_min_and_max()
        self.y_axis_width = 80
        self.x_axis_height = 40
        self.draw_x_axis = False
        self.draw_y_axis = False
        self.mouse_draw_event = None
        self.num_horizontal_gridlines = 8
        self.gridline_datapoints: list[int] = []
        self._draw_gridlines = True
        self._draw__vertical_cursor = True
        self._draw__horizontal_cursor = True
        self.mouse_enter_event = None
        self.mouse_leave_event = None
        self._x_axis_labels: list[str] = None
        self.index_change_event = None
        self.labels = []

    def set_data(self, title: str, data: list[float], rgba: RGBA):
        self.create_dataset(title, data, rgba)
        self.update()

    def create_dataset(self, title: str, data: list[float], rgba: RGBA):
        self.dataset = DataSet(title, data, rgba)

    def clear_datasets(self):
        self.dataset.clear()
        self.labels.clear()
        title, data, rgba = self.initial_data
        self.create_dataset(title, data, rgba)
        self.set_indexes(0, 1)
        self.recalc_min_and_max()
        self.update()

    def set_x_axis_labels(self, labels: list[str]):
        self._x_axis_labels = labels

    @overrides
    def enterEvent(self, a0: QtCore.QEvent) -> None:
        super().enterEvent(a0)
        self.set_draw_vertical_cursor(True)
        self.set_draw_horizontal_cursor(True)
        if self.mouse_enter_event is not None:
            self.mouse_enter_event(self)

    @overrides
    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        super(LineChart, self).leaveEvent(a0)
        self.set_draw_vertical_cursor(False)
        self.set_draw_horizontal_cursor(False)
        self.update()
        if self.mouse_leave_event is not None:
            self.mouse_leave_event(self)

    def set_draw_vertical_cursor(self, draw: bool):
        self._draw__vertical_cursor = draw

    def set_draw_horizontal_cursor(self, draw: bool):
        self._draw__horizontal_cursor = draw

    def set_mouse_x(self, x: int):
        self._mouse_x = x
        self.update()

    def set_mouse_y(self, y: int):
        self._mouse_y = y
        self.update()

    def set_draw_gridlines(self, draw: bool):
        self._draw_gridlines = draw

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

    #  use this only if you know what you are doing
    def set_indexes(self, first_index: int, last_index: int):
        self.first_index = first_index
        self.last_index = last_index

        self.recalc_min_and_max()
        self.recalc_gridline_indexes()
        self.update()

    def change_first_index(self, increment: bool):
        if increment:
            self.first_index += 1
        else:
            self.first_index -= 1
        self.recalc_min_and_max()
        self.recalc_gridline_indexes()
        if self.index_change_event:
            self.index_change_event(self.first_index, self.last_index)

    def change_last_index(self, increment: bool):
        if increment:
            self.last_index += 1
        else:
            self.last_index -= 1
        self.recalc_min_and_max()
        self.recalc_gridline_indexes()
        if self.index_change_event:
            self.index_change_event(self.first_index, self.last_index)

    def zoom_out_max(self):
        while self.num_datapoints_on_screen() < self.dataset.collection_length() - 1 and self.num_datapoints_on_screen() < self.max_datapoints_on_screen:
            self.zoom_out()


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
        num_points = self.last_index - self.first_index
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

        self._mouse_x = a0.x()
        self._mouse_y = a0.y()

        if self.index_change_event is not None:
            self.index_change_event(self.first_index, self.last_index)
        if self.mouse_draw_event is not None:
            self.mouse_draw_event(self._mouse_x, self._mouse_y, self)

        self.update()

    @overrides
    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        super().wheelEvent(a0)
        if self.handle_mouse_events:
            if self.index_change_event is not None:
                self.index_change_event(self.first_index, self.last_index)

    def draw_mouse_cursor(self):
        if self._draw__vertical_cursor:
            self.draw_vertical_mouse_line(self._mouse_x)
        if self._draw__horizontal_cursor:
            self.draw_horizontal_mouse_line(self._mouse_y)

    def draw_horizontal_mouse_line(self, y: int):
        if self._mouse_x > self.chart_width() or self._mouse_y > self.chart_height():
            return
        self.painter.setPen(QPen(StyleInfo.color_cursor, StyleInfo.pen_width, Qt.DashLine))
        # draw horizontal line
        x1 = 0
        x2 = self.chart_width()
        self.painter.drawLine(x1, y, x2, y)
        self.draw_y_axis_label(self.convert_y_to_value(self._mouse_y), self._mouse_y, Qt.white)

    def draw_vertical_mouse_line(self, x: int):
        if self._mouse_x > self.chart_width() or self._mouse_y > self.chart_height():
            return
        self.painter.setPen(QPen(StyleInfo.color_cursor, StyleInfo.pen_width, Qt.DashLine))
        index, datapoint_for_x = self.get_datapoint_for_x(x)
        y1 = 0
        y2 = self.chart_height()
        self.painter.drawLine(datapoint_for_x, y1, datapoint_for_x, y2)
        if self._x_axis_labels:
            self.draw_x_axis_label(index, self.get_x_for_index(index), self.format_text_for_x_axis(index))
        self.draw_horizontal_indicator_lines()

    def draw_x_axis_label(self, index: int, x: int, text: str):
        self.painter.setPen(QPen(Qt.white, .01, Qt.SolidLine))
        self.painter.setBrush(QBrush(StyleInfo.color_background, Qt.SolidPattern))

        w = 100
        y = self.chart_height()
        x = x - int(w / 2)
        h = self.x_axis_height
        self.painter.drawRect(x, y, w, h)
        self.painter.drawText(QRectF(x, y, w, h), Qt.AlignHCenter | Qt.AlignCenter, text)

    def add_collection(self, title: str, data: list[float], rgb: RGBA):
        self.dataset.add_collection(title, data, rgb)
        self.recalc_min_and_max()

    def get_y_for_datapoint(self, item: float) -> int:
        height = item - self.min_value_on_screen
        delta = self.max_value_on_screen - self.min_value_on_screen
        if delta != 0:
            return self.chart_height() - int((height / delta) * self.chart_height())
        else:
            return self.chart_height() - int(self.chart_height() / 2)

    def get_x_for_index(self, i: int):
        length = self.num_datapoints_on_screen()
        index_on_screen = i - self.first_index + 1
        return int((index_on_screen / length) * self.chart_width()) - int(self.datapoint_width() / 2.0)

    # take in an x pixel location and return the x pixel location of the closest datapoint
    def get_datapoint_for_x(self, x: int) -> (int, int):
        percent = x / self.chart_width()
        index = int(percent * self.num_datapoints_on_screen())
        return self.first_index + index, self.get_x_for_index(self.first_index + index)

    def draw_datapoint(self, i: int, collection: Collection):
        self.painter.setPen(QPen(collection.color.color(), StyleInfo.pen_width, Qt.SolidLine))
        first = collection[i]
        second = collection[i + 1]

        x1 = self.get_x_for_index(i)
        y1 = self.get_y_for_datapoint(first)
        x2 = self.get_x_for_index(i + 1)
        y2 = self.get_y_for_datapoint(second)
        self.painter.drawLine(x1, y1, x2, y2)

    def draw_label(self, label: Label):
        y = self.get_y_for_datapoint(label.y_value)
        # w = self.datapoint_width()
        # if w < 50:
        #     w = 50
        w = 50
        x = self.get_x_for_index(label.x_index) - int(w / 2.0)
        triangle_height = 15
        square_height = 35

        if self.get_x_for_index(label.x_index) > self.chart_width():
            return

        self.painter.setPen(QPen(Qt.white, .01, Qt.SolidLine))
        self.painter.setBrush(QBrush(label.color, Qt.SolidPattern))

        rect = QRectF(x, y, w, triangle_height)

        path = QPainterPath()
        path.moveTo(rect.left() + (rect.width() / 2), rect.top())
        path.lineTo(rect.bottomLeft())
        path.lineTo(rect.bottomRight())
        path.lineTo(rect.left() + (rect.width() / 2), rect.top())

        self.painter.fillPath(path, label.color)

        self.painter.drawRect(x, y + triangle_height, w, square_height)
        self.painter.drawText(QRectF(x, y + triangle_height, w, square_height), Qt.AlignHCenter | Qt.AlignVCenter, label.text)

    def add_label(self, y_value: float, x_index: int, text: str, buy: bool):
        if buy:
            color = StyleInfo.color_green_candle()
        else:
            color = StyleInfo.color_red_candle()
        color.setAlpha(100)
        self.labels.append(Label(y_value, x_index, text, color))

    def recalc_gridline_indexes(self):
        if self._draw_gridlines:
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
        if self._draw_gridlines:
            for index in self.gridline_datapoints:
                if self.first_index < index < self.last_index:
                    x = self.get_x_for_index(index)
                    self.painter.setPen(QPen(StyleInfo.color_grid_line, StyleInfo.gridline_width, Qt.SolidLine))
                    self.painter.drawLine(x, 0, x, self.chart_height())

                    # find x axis value
                    self.painter.setPen(QPen(QColor(255, 255, 255), .05, Qt.SolidLine))
                    self.draw_x_axis_label(index, x, self.format_text_for_x_axis(index))

    def format_text_for_x_axis(self, index: int) -> str:
        if self._x_axis_labels is not None and index < len(self._x_axis_labels):
            return self._x_axis_labels[index]
        return str(index)

    def format_text_for_y_axis(self, text: float) -> str:
        return str(text)  # override to change the format for the y axis labels

    def convert_y_to_value(self, y: float):
        if y != 0 and self.max_value_on_screen - self.min_value_on_screen != 0:
            return self.min_value_on_screen + ((self.chart_height() - y) / self.chart_height() * (self.max_value_on_screen - self.min_value_on_screen))
        else:
            return 0

    def draw_y_axis_label(self, value: float, y: int, color: QColor):
        self.painter.setPen(QPen(color, .01, Qt.SolidLine))
        self.painter.setBrush(QBrush(StyleInfo.color_background, Qt.SolidPattern))

        h = 20
        x = self.chart_width()
        y = int(y - h / 2)
        w = self.width() - self.chart_width()
        self.painter.drawRect(x, y, w, h)
        self.painter.drawText(QRectF(x, y, w, h),
                              Qt.AlignHCenter | Qt.AlignCenter,
                              self.format_text_for_y_axis(value))

    def draw_gridlines(self):
        self.draw_horizontal_gridlines()
        self.draw_vertical_gridlines()

    def draw_horizontal_gridlines(self):
        if self._draw_gridlines:
            num_labels_on_y_axis = self.num_horizontal_gridlines
            for i in range(int(num_labels_on_y_axis)):
                x1 = 0
                x2 = self.chart_width()
                y1 = int(i * (self.chart_height() / num_labels_on_y_axis)) + int(
                    (self.chart_height() / num_labels_on_y_axis) / 2)
                y2 = y1
                self.painter.setPen(QPen(StyleInfo.color_grid_line, StyleInfo.gridline_width, Qt.SolidLine))
                self.painter.drawLine(x1, y1, x2, y2)
                self.draw_y_axis_label(self.convert_y_to_value(y1), y1, Qt.white)

    # horizontal lines and labels for indicators
    def draw_horizontal_indicator_lines(self):
        i = 0
        for collection in self.dataset.collections():
            if collection.color.a == 0:
                continue
            index, x = self.get_datapoint_for_x(self._mouse_x)
            if index < len(collection):
                point = collection[index]
                y_value = self.get_y_for_datapoint(point)
                self.painter.setPen(QPen(collection.get_qcolor(), StyleInfo.pen_width, Qt.DashLine))
                # self.painter.drawLine(x, y_value, self.chart_width(), y_value)
                self.draw_y_axis_label(point, y_value, collection.get_qcolor())

                price_str = self.format_text_for_y_axis(point)
                font = QFont("times", 12)
                fm = QFontMetrics(font)
                text = f"{collection.title} {price_str}"
                text_height = 20
                x = 5
                y = i * text_height
                w = fm.width(text)
                h = text_height
                self.painter.drawRect(x, y, w, h)
                self.painter.drawText(QRectF(x, y, w, h), Qt.AlignVCenter | Qt.AlignLeft,
                                      text)
                i += 1

    def draw_collections(self):

        collection: Collection
        collections = self.dataset.collections()
        for i in range(len(collections)):
            collection: Collection = collections[i]
            if len(collection) > 1:
                for j in range(self.first_index, self.last_index - 1):
                    self.draw_datapoint(j, collection)

    def draw_labels(self):
        for label in self.labels:
            self.draw_label(label)

    @overrides
    def draw_objects(self):
        self.draw_gridlines()
        self.draw_collections()
        self.draw_labels()
        self.draw_mouse_cursor()
