from Controls.Panel import Panel
from DataClasses.Candle import Candle
from Controls.CandleChart import CandleChart, LineChart
from DataClasses.RGBA import RGBA
from Controls.Splitter import Splitter
from Controls.LayoutDirection import LayoutDirection
from Controls.IndicatorChart import IndicatorChart
from Controls.TimeframePanel import TimeframePanel


class ChartAndIndicator(Panel):
    def __init__(self, data: list[Candle]):
        super().__init__()
        self.__candle_chart = CandleChart(data)
        self.__indicator_charts: list[IndicatorChart] = []

        self.splitter = Splitter(LayoutDirection.VERTICAL)
        self.add_widget(self.splitter)
        self.splitter.addWidget(self.__candle_chart)

        self.x_axis_labels = []
        for can in data:
            self.x_axis_labels.append(can.date_time())

        low: list[float] = []
        for can in data:
            low.append(can.low())
        # self.__indicator_chart = IndicatorChart("LOWS", low, RGBA(255, 0, 0, 255))
        self.create_new_indicator_chart("LOWS", low, RGBA(255, 0, 0, 255))

        high: list[float] = []
        for can in data:
            high.append(can.high())
        # self.__indicator_chart.add_collection("HIGHS", high, RGBA(0, 255, 0, 255))
        self.add_indicator("HIGHS", high, RGBA(0, 255, 0, 255), 0)

        # labels = []
        # for can in data:
        #     labels.append(can.date_time())
        # self.__indicator_chart.set_x_axis_labels(labels)
        # self.__indicator_charts[0].set_x_axis_labels(labels)

        # self.splitter.addWidget(self.__indicator_chart)

        self.timeframe_panel = TimeframePanel()
        self.add_widget(self.timeframe_panel)

        self.__candle_chart.resize(self.width(), int(self.height() * .75))
        # self.__indicator_chart.resize(self.width(), int(self.height() * .25))
        self.__indicator_charts[0].resize(self.width(), int(self.height() * .25))

        self.__candle_chart.set_draw_y_axis(True)
        # self.__indicator_chart.set_draw_y_axis(True)
        # self.__indicator_chart.set_draw_x_axis(True)

        self.__candle_chart.mouse_enter_event = self.candle_chart_mouse_enter_event
        # self.__indicator_chart.mouse_enter_event = self.indicator_chart_mouse_enter_event

        self.__candle_chart.mouse_leave_event = self.candle_chart_mouse_leave_event
        # self.__indicator_chart.mouse_leave_event = self.indicator_chart_mouse_leave_event

    def clear_indicators(self):
        for i in range(len(self.__indicator_charts)):
            widget = self.splitter.widget(i + 1)
            widget.deleteLater()

        self.__indicator_charts.clear()

    def create_new_indicator_chart(self, title: str, data: list[float], rgba: RGBA):
        if len(data) != self.__candle_chart.dataset.collection_length():
            raise ValueError("Indicators must have a datapoint for every candle")
        indicator_chart = IndicatorChart(title, data, rgba)
        indicator_chart.set_x_axis_labels(self.x_axis_labels)
        indicator_chart.set_draw_y_axis(True)
        indicator_chart.set_draw_x_axis(True)
        indicator_chart.set_indexes(self.__candle_chart.first_index, self.__candle_chart.last_index)
        indicator_chart.mouse_enter_event = self.indicator_chart_mouse_enter_event
        indicator_chart.mouse_leave_event = self.indicator_chart_mouse_leave_event

        self.__indicator_charts.append(indicator_chart)
        self.splitter.addWidget(indicator_chart)

    def add_collection(self, title: str, data: list[float], rgba: RGBA):
        self.__candle_chart.add_collection(title, data, rgba)

    def add_indicator(self, title: str, data: list[float], rgba: RGBA, index: int):
        if index < 0:
            raise ValueError("Index cannot be zero")
        if index > len(self.__indicator_charts):
            raise ValueError("Cannot skip index")
        if index == len(self.__indicator_charts):
            self.create_new_indicator_chart(title, data, rgba)
        self.__indicator_charts[index].add_collection(title, data, rgba)

        # self.__indicator_chart.add_collection(title, data, rgba)

    def indicator_checked(self, indicator_name: str, checked: bool):
        match indicator_name:
            case "Bollinger Bands":
                self.__candle_chart.bollinger_bands(20, 2)
                return

    def clear_strategy(self):
        self.clear_indicators()
        self.__candle_chart.clear_datasets()

    def indicator_chart_mouse_enter_event(self):
        for indicator_chart in self.__indicator_charts:
            indicator_chart.change_first_index_event = self.indicator_chart_change_fist_index_event
            indicator_chart.change_last_index_event = self.indicator_chart_change_last_index_event
            indicator_chart.mouse_draw_event = self.indicator_chart_mouse_draw_event

        # self.__indicator_chart.change_first_index_event = self.indicator_chart_change_fist_index_event
        # self.__indicator_chart.change_last_index_event = self.indicator_chart_change_last_index_event
        # self.__indicator_chart.mouse_draw_event = self.indicator_chart_mouse_draw_event

    def indicator_chart_mouse_leave_event(self):
        for indicator_chart in self.__indicator_charts:
            indicator_chart.change_first_index_event = None
            indicator_chart.change_last_index_event = None
            indicator_chart.mouse_draw_event = None

        # self.__indicator_chart.change_first_index_event = None
        # self.__indicator_chart.change_last_index_event = None
        # self.__indicator_chart.mouse_draw_event = None

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
        for indicator_chart in self.__indicator_charts:
            indicator_chart.set_draw_vertical_cursor(True)
            indicator_chart.set_draw_horizontal_cursor(False)
            indicator_chart.set_mouse_x(x)

        # self.__indicator_chart.set_draw_vertical_cursor(True)
        # self.__indicator_chart.set_draw_horizontal_cursor(False)
        # self.__indicator_chart.set_mouse_x(x)

    def candle_chart_change_fist_index_event(self, increment: bool):
        for indicator_chart in self.__indicator_charts:
            indicator_chart.change_first_index(increment)

        # self.__indicator_chart.change_first_index(increment)

    def candle_chart_change_last_index_event(self, increment: bool):
        for indicator_chart in self.__indicator_charts:
            indicator_chart.change_last_index(increment)

        # self.__indicator_chart.change_last_index(increment)

    def candle_chart(self):
        return self.__candle_chart

