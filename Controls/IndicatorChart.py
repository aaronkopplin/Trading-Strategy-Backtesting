from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import StyleInfo
from Controls.Panel import Panel
from DataClasses.DataSet import DataSet
from DataClasses.Account import Account
from Controls.LineChart import LineChart
from DataClasses.Candle import Candle
from overrides import overrides
from DataClasses.RGBA import RGBA
import datetime
from Utilities.TextUtilities import convert_price_to_str


class IndicatorChart(LineChart):
    def __init__(self, title: str, data: list[float], rgba: RGBA):
        super().__init__(title, data, rgba)
        self.index = 0

    @overrides
    def draw_mouse_cursor(self):
        if self._draw__vertical_cursor:
            self.draw_vertical_mouse_line(self._mouse_x)
        if self._draw__horizontal_cursor:
            self.draw_horizontal_mouse_line(self._mouse_y)

    @overrides
    def format_text_for_y_axis(self, text: float) -> str:
        return convert_price_to_str(text)

    @overrides
    def format_text_for_x_axis(self, index: int) -> str:
        if index < len(self._x_axis_labels):
            date_time = self._x_axis_labels[index]
            date_time = datetime.datetime.strptime(date_time[:len(date_time) - 6], '%Y-%m-%d %H:%M:%S').strftime(
                '%d %H:%M')
            return date_time
        else:
            return ""
