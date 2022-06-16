from Controls.Panel import Panel
from DataClasses.Candle import Candle
from Controls.CandleChart import CandleChart, LineChart
from DataClasses.RGBA import RGBA
from Controls.Splitter import Splitter
from Controls.LayoutDirection import LayoutDirection
from Controls.IndicatorChart import IndicatorChart
from Controls.TimeframePanel import TimeframePanel
import yfinance as yf, pandas as pd


class ChartAndIndicator(Panel):
    def __init__(self):
        super().__init__()
        self.indicator_charts: list[IndicatorChart] = []
        self.splitter = Splitter(LayoutDirection.VERTICAL)
        self.add_widget(self.splitter)

        # event fired when submit is hit on timeframe panel, and new data is available.
        self.data_change_event = None

        self.candles = []
        self.candle_chart: CandleChart = None
        self.timeframe_panel = TimeframePanel()
        self.timeframe_panel.submit_event = self.submit_event
        self.timeframe_panel.run_query()

        self.splitter.addWidget(self.candle_chart)

        self.x_axis_labels = []
        for can in self.candles:
            self.x_axis_labels.append(can.date_time())

        low: list[float] = []
        for can in self.candles:
            low.append(can.low())
        self.create_new_indicator_chart("LOWS", low, RGBA(255, 0, 0, 255))

        high: list[float] = []
        for can in self.candles:
            high.append(can.high())
        self.add_indicator("HIGHS", high, RGBA(0, 255, 0, 255), 0)

        self.add_widget(self.timeframe_panel)

        self.candle_chart.resize(self.width(), int(self.height() * .75))
        self.indicator_charts[0].resize(self.width(), int(self.height() * .25))

        self.candle_chart.set_draw_y_axis(True)
        self.candle_chart.index_change_event = lambda f, l: self.candle_chart_index_change_event(f, l)
        self.candle_chart.mouse_draw_event = lambda x, y, c: self.candle_chart_mouse_draw_event(x, y, c)

        self.candle_chart.zoom_out_max()

    def submit_event(self, mom_data: pd.DataFrame):
        candles = []
        for row in mom_data.iloc:
            date_time = str(row.name)
            open = row.Open
            high = row.High
            low = row.Low
            close = row.Close
            adj_close = 0
            volume = row.Volume
            candle = Candle([date_time, open, high, low, close, adj_close, volume])
            candles.append(candle)

        self.candles = candles
        if self.candle_chart is None:
            self.candle_chart = CandleChart(candles)
        else:
            self.candle_chart.set_data(candles)

        if self.data_change_event:
            self.data_change_event()

        # todo: replace with logic that updates the indicators with the appropriate new data. someday...
        self.clear_indicators()

    def clear_indicators(self):
        for i in range(len(self.indicator_charts)):
            widget = self.splitter.widget(i + 1)
            widget.deleteLater()

        self.indicator_charts.clear()

    def create_new_indicator_chart(self, title: str, data: list[float], rgba: RGBA):
        if len(data) != self.candle_chart.dataset.collection_length():
            raise ValueError("Indicator must have a datapoint for every candle") # todo: remove initial_data, replace with remove indicators rather than initial data
        indicator_chart = IndicatorChart(title, data, rgba)
        indicator_chart.set_x_axis_labels(self.x_axis_labels)
        indicator_chart.set_draw_y_axis(True)
        indicator_chart.set_indexes(self.candle_chart.first_index, self.candle_chart.last_index)

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
        self.candle_chart.set_draw_vertical_cursor(True)
        self.candle_chart.set_mouse_x(x)
        for chart in self.indicator_charts:
            if chart is not caller:
                chart.set_draw_vertical_cursor(True)
                chart.set_mouse_x(x)

    def candle_chart_mouse_draw_event(self, x: int, y: int, caller: LineChart):
        for chart in self.indicator_charts:
            chart.set_draw_vertical_cursor(True)
            chart.set_mouse_x(x)

    def add_collection(self, title: str, data: list[float], rgba: RGBA):
        self.candle_chart.add_collection(title, data, rgba)

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
                self.candle_chart.bollinger_bands(20, 2)
                return

    def clear_strategy(self):
        self.clear_indicators()
        self.candle_chart.clear_datasets()
        self.candle_chart.zoom_out_max()

    def candle_chart_index_change_event(self, first_index, last_index):
        for indicator_chart in self.indicator_charts:
            indicator_chart.set_indexes(first_index, last_index)

    def indicator_chart_index_change_event(self, first_index, last_index):
        self.candle_chart.set_indexes(first_index, last_index)
        for indicator_chart in self.indicator_charts:
            indicator_chart.set_indexes(first_index, last_index)

    def candle_chart(self):
        return self.candle_chart

    def zoom_max(self):
        self.candle_chart.zoom_out_max()
        for chart in self.indicator_charts:
            chart.update()

    def add_label(self, price: float, index: int, text: str, buy: bool):
        self.candle_chart.add_label(price, index, text, buy)

