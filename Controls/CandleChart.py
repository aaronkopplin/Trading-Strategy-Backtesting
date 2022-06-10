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
from Indicator.BollingerBands import bollinger_bands
from Utilities.TextUtilities import convert_price_to_str


# handle drawing candles on top of data
class CandleChart(LineChart):
    def __init__(self, data: list[Candle]):
        self.candles = data
        closes = []
        labels = []
        for can in data:
            closes.append(can.close())
            labels.append(can.date_time())
        super().__init__("", closes, RGBA(255, 255, 255,  0))

        self.set_x_axis_labels(labels)

    def set_data(self, data: list[Candle]):
        closes = []
        labels = []
        for can in data:
            closes.append(can.close())
            labels.append(can.date_time())

        self.candles = data
        self.create_dataset("", closes, RGBA(255, 255, 255,  0))
        self.set_x_axis_labels(labels)
        self.update()

    def bollinger_bands(self, length: int, stdev: int):
        lower_band, middle, upper_band = bollinger_bands(self.candles, length, stdev)
        self.add_collection("UPPER BOLLINGER", upper_band, RGBA(51, 190, 255, 255))
        self.add_collection("MIDDLE BOLLINGER", middle, RGBA(255, 188, 51, 255))
        self.add_collection("LOWER BOLLINGER", lower_band, RGBA(51, 190, 255, 255))

    def min_candle_value_between_indexes(self):
        can: Candle
        return min([can.low() for can in self.candles[self.first_index:self.last_index]])

    def max_candle_value_between_indexes(self):
        can: Candle
        return max([can.high() for can in self.candles[self.first_index:self.last_index]])

    @overrides
    def recalc_min_and_max(self):
        min_dataset_value = self.dataset.min_value_between_indexes(self.first_index, self.last_index)
        max_dataset_value = self.dataset.max_value_between_indexes(self.first_index, self.last_index)
        self.min_value_on_screen = min(self.min_candle_value_between_indexes(), min_dataset_value)
        self.max_value_on_screen = max(self.max_candle_value_between_indexes(), max_dataset_value)

    def draw_candle(self, i: int):
        can: Candle = self.candles[i]

        x = self.get_x_for_index(i)
        y1 = int(self.get_y_for_datapoint(can.low()))
        y2 = int(self.get_y_for_datapoint(can.high()))

        if can.close() <= can.open():
            self.painter.setPen(QPen(StyleInfo.color_red_candle(), StyleInfo.pen_width, Qt.SolidLine))
            self.painter.setBrush(QBrush(StyleInfo.color_background, Qt.SolidPattern))
        else:
            self.painter.setPen(QPen(StyleInfo.color_green_candle(), StyleInfo.pen_width, Qt.SolidLine))
            self.painter.setBrush(QBrush(StyleInfo.color_background, Qt.SolidPattern))
        self.painter.drawLine(x, y1, x, y2)

        x = x - int(self.datapoint_width() / 2.0)
        y = int(self.get_y_for_datapoint(min(can.open(), can.close())))
        w = self.datapoint_width()
        top = self.get_y_for_datapoint(max(can.open(), can.close()))
        bottom = self.get_y_for_datapoint(min(can.open(), can.close()))
        h = int(top - bottom)

        self.painter.drawRect(x, y, w, h)

    def draw_candles(self):
        for i in range(self.first_index, self.last_index ):
            self.draw_candle(i)

    @overrides
    def format_text_for_y_axis(self, text: float) -> str:
        return convert_price_to_str(text)

    @overrides
    def draw_objects(self):
        self.draw_horizontal_gridlines()
        self.draw_vertical_gridlines()
        self.draw_candles()
        self.draw_collections()
        self.draw_labels()
        self.draw_mouse_cursor()
