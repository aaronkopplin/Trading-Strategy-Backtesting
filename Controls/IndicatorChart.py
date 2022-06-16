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
    def format_text_for_y_axis(self, text: any) -> str:
        return convert_price_to_str(text)

    @overrides
    def format_text_for_x_axis(self, index: int) -> str:
        if self._x_axis_labels and index < len(self._x_axis_labels):
            return str(self._x_axis_labels[index]).replace("00:00:00", "").replace(" ", "")
