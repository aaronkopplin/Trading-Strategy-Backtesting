from Controls.Panel import Panel
from DataClasses.Candle import Candle
from Controls.CandleChart import CandleChart, LineChart
from DataClasses.RGBA import RGBA
from Controls.Splitter import Splitter
from Controls.LayoutDirection import LayoutDirection
from Controls.IndicatorChart import IndicatorChart


class ChartAndIndicator(Panel):
    def __init__(self, data: list[Candle]):
        super().__init__()
        self.__candle_chart = CandleChart(data)
        low: list[float] = []
        for can in data:
            low.append(can.low())
        self.__indicator_chart = IndicatorChart(low, RGBA(255, 0, 0, 255))

        high: list[float] = []
        for can in data:
            high.append(can.high())
        self.__indicator_chart.add_collection(high, RGBA(0, 255, 0, 255))

        labels = []
        for can in data:
            labels.append(can.date_time())
        self.__indicator_chart.set_x_axis_labels(labels)

        self.splitter = Splitter(LayoutDirection.VERTICAL)
        self.add_widget(self.splitter)
        self.splitter.addWidget(self.__candle_chart)
        self.splitter.addWidget(self.__indicator_chart)

        self.__candle_chart.resize(self.width(), int(self.height() * .75))
        self.__indicator_chart.resize(self.width(), int(self.height() * .25))

        self.__candle_chart.set_draw_y_axis(True)
        self.__indicator_chart.set_draw_y_axis(True)
        self.__indicator_chart.set_draw_x_axis(True)

        self.__candle_chart.mouse_enter_event = self.candle_chart_mouse_enter_event
        self.__indicator_chart.mouse_enter_event = self.indicator_chart_mouse_enter_event

        self.__candle_chart.mouse_leave_event = self.candle_chart_mouse_leave_event
        self.__indicator_chart.mouse_leave_event = self.indicator_chart_mouse_leave_event

    def indicator_chart_mouse_enter_event(self):
        self.__indicator_chart.change_first_index_event = self.indicator_chart_change_fist_index_event
        self.__indicator_chart.change_last_index_event = self.indicator_chart_change_last_index_event
        self.__indicator_chart.mouse_draw_event = self.indicator_chart_mouse_draw_event

    def indicator_chart_mouse_leave_event(self):
        self.__indicator_chart.change_first_index_event = None
        self.__indicator_chart.change_last_index_event = None
        self.__indicator_chart.mouse_draw_event = None

    def candle_chart_mouse_enter_event(self):
        self.__candle_chart.change_first_index_event = self.candle_chart_change_fist_index_event
        self.__candle_chart.change_last_index_event = self.candle_chart_change_last_index_event
        self.__candle_chart.mouse_draw_event = self.candle_chart_mouse_draw_event

    def candle_chart_mouse_leave_event(self):
        self.__candle_chart.change_first_index_event = None
        self.__candle_chart.change_last_index_event = None
        self.__candle_chart.mouse_draw_event = None

    def indicator_chart_mouse_draw_event(self, x: int, y: int):
        self.__candle_chart.set_draw_vertical_cursor(True)
        self.__candle_chart.set_draw_horizontal_cursor(False)
        self.__candle_chart.set_mouse_x(x)

    def indicator_chart_change_fist_index_event(self, increment: bool):
        self.__candle_chart.change_first_index(increment)

    def indicator_chart_change_last_index_event(self, increment: bool):
        self.__candle_chart.change_last_index(increment)

    def candle_chart_mouse_draw_event(self, x: int, y: int):
        self.__indicator_chart.set_draw_vertical_cursor(True)
        self.__indicator_chart.set_draw_horizontal_cursor(False)
        self.__indicator_chart.set_mouse_x(x)

    def candle_chart_change_fist_index_event(self, increment: bool):
        self.__indicator_chart.change_first_index(increment)

    def candle_chart_change_last_index_event(self, increment: bool):
        self.__indicator_chart.change_last_index(increment)

    def candle_chart(self):
        return self.__candle_chart

