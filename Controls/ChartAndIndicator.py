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
from Controls.CandleChart import CandleChart, LineChart
from overrides import overrides
from DataClasses.RGBA import RGBA
from Controls.Splitter import Splitter
from Controls.LayoutDirection import LayoutDirection


class ChartAndIndicator(Panel):
    def __init__(self, data: list[Candle]):
        super().__init__()
        self.__candle_chart = CandleChart(data)
        low: list[float] = []
        for can in data:
            low.append(can.low())
        self.__indicator_chart = LineChart(low, RGBA(255, 0, 0, 255))

        high: list[float] = []
        for can in data:
            high.append(can.high())
        self.__indicator_chart.add_collection(high, RGBA(0, 255, 0, 255))

        self.__indicator_chart.set_draw_gridlines(False)

        self.splitter = Splitter(LayoutDirection.VERTICAL)
        self.add_widget(self.splitter)
        self.splitter.addWidget(self.__candle_chart)
        self.splitter.addWidget(self.__indicator_chart)

        self.__candle_chart.resize(self.width(), int(self.height() * .75))
        self.__indicator_chart.resize(self.width(), int(self.height() * .25))

        self.__candle_chart.set_draw_y_axis(True)
        self.__indicator_chart.set_draw_y_axis(True)
        self.__indicator_chart.set_draw_x_axis(True)

        self.__candle_chart.change_first_index_event = self.change_fist_index_event
        self.__candle_chart.change_last_index_event = self.change_last_index_event

        self.__indicator_chart.set_handle_mouse_events(False)

    def change_fist_index_event(self, increment: bool):
        self.__indicator_chart.change_first_index(increment)

    def change_last_index_event(self, increment: bool):
        self.__indicator_chart.change_last_index(increment)

    def candle_chart(self):
        return self.__candle_chart

