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
        self.indicator_charts: list[IndicatorChart] = []
        self.splitter = Splitter(LayoutDirection.VERTICAL)
        self.add_widget(self.splitter)

        self.__candle_chart = CandleChart(data)
        self.splitter.addWidget(self.__candle_chart)

        self.x_axis_labels = []
        for can in data:
            self.x_axis_labels.append(can.date_time())

        low: list[float] = []
        for can in data:
            low.append(can.low())
        self.create_new_indicator_chart("LOWS", low, RGBA(255, 0, 0, 255))

        high: list[float] = []
        for can in data:
            high.append(can.high())
        self.add_indicator("HIGHS", high, RGBA(0, 255, 0, 255), 0)

        self.timeframe_panel = TimeframePanel()
        self.add_widget(self.timeframe_panel)

        self.__candle_chart.resize(self.width(), int(self.height() * .75))
        self.indicator_charts[0].resize(self.width(), int(self.height() * .25))

        self.__candle_chart.set_draw_y_axis(True)
        self.__candle_chart.index_change_event = lambda f, l: self.candle_chart_index_change_event(f, l)
        self.__candle_chart.mouse_draw_event = lambda x, y ,c: self.candle_chart_mouse_draw_event(x, y, c)

        self.__candle_chart.zoom_out_max()

    def clear_indicators(self):
        for i in range(len(self.indicator_charts)):
            widget = self.splitter.widget(i + 1)
            widget.deleteLater()

        self.indicator_charts.clear()

    def create_new_indicator_chart(self, title: str, data: list[float], rgba: RGBA):
        if len(data) != self.__candle_chart.dataset.collection_length():
            raise ValueError("Indicator must have a datapoint for every candle")
        indicator_chart = IndicatorChart(title, data, rgba)
        indicator_chart.set_x_axis_labels(self.x_axis_labels)
        indicator_chart.set_draw_y_axis(True)
        indicator_chart.set_indexes(self.__candle_chart.first_index, self.__candle_chart.last_index)

        indicator_chart.mouse_draw_event = lambda x, y, c: self.indicator_chart_mouse_draw_event(x, y, c)
        indicator_chart.index_change_event = lambda f, l: self.indicator_chart_index_change_event(f, l)

        indicator_chart.index = len(self.indicator_charts)
        self.indicator_charts.append(indicator_chart)
        self.splitter.addWidget(indicator_chart)

        for ic in self.indicator_charts:
            ic.set_draw_x_axis(False)
            ic.setMinimumHeight(200)
        indicator_chart.set_draw_x_axis(True)

    def indicator_chart_mouse_draw_event(self, x: int, y: int, caller: IndicatorChart):
        self.__candle_chart.set_draw_vertical_cursor(True)
        self.__candle_chart.set_mouse_x(x)
        for chart in self.indicator_charts:
            if chart is not caller:
                chart.set_draw_vertical_cursor(True)
                chart.set_mouse_x(x)

    def candle_chart_mouse_draw_event(self, x: int, y: int, caller: LineChart):
        for chart in self.indicator_charts:
            chart.set_draw_vertical_cursor(True)
            chart.set_mouse_x(x)

    def add_collection(self, title: str, data: list[float], rgba: RGBA):
        self.__candle_chart.add_collection(title, data, rgba)

    def add_indicator(self, title: str, data: list[float], rgba: RGBA, index: int):
        if index < 0:
            raise ValueError("Index cannot be zero")
        if index > len(self.indicator_charts):
            raise ValueError("Cannot skip index")
        if index == len(self.indicator_charts):
            self.create_new_indicator_chart(title, data, rgba)
        self.indicator_charts[index].add_collection(title, data, rgba)

    def indicator_checked(self, indicator_name: str, checked: bool):
        match indicator_name:
            case "Bollinger Bands":
                self.__candle_chart.bollinger_bands(20, 2)
                return

    def clear_strategy(self):
        self.clear_indicators()
        self.__candle_chart.clear_datasets()

    def candle_chart_index_change_event(self, first_index, last_index):
        for indicator_chart in self.indicator_charts:
            indicator_chart.set_indexes(first_index, last_index)

    def indicator_chart_index_change_event(self, first_index, last_index):
        self.__candle_chart.set_indexes(first_index, last_index)
        for indicator_chart in self.indicator_charts:
            indicator_chart.set_indexes(first_index, last_index)

    def candle_chart(self):
        return self.__candle_chart

    def zoom_max(self):
        self.__candle_chart.zoom_out_max()
        for chart in self.indicator_charts:
            chart.update()

    def draw_label(self, price: float, index: int, text: str):
        self.__candle_chart.add_label(price, index, text)

