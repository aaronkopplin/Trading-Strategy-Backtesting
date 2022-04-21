import csv
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import date, timedelta
from datetime import datetime

from Candle import Candle
from CandleChart import CandleChart
from Strategy import Account, Trade
from TimeframePanel import TimeframePanel
from Controls.Panel import Panel
from Controls.LayoutDirection import LayoutDirection
from Controls.Splitter import Splitter


class Graph(Panel):
    def __init__(self, candles: list):
        super().__init__()
        self.candles = candles
        self.chart = CandleChart(candles)
        self.detect_trends()

        self.timeframe_panel = TimeframePanel(self.chart)
        self.timeframe_panel.setFixedHeight(40)
        self.timeframe_panel.submit_event = self.submit_event
        self.add_widget(self.timeframe_panel)

        self.chart_options = Panel()
        self.chart_options.set_layout(LayoutDirection.HORIZONTAL)
        self.bollinger_bands_check = QCheckBox("Bollinger Bands")
        self.bollinger_bands_check.clicked.connect(self.draw_bollinger_bands)
        self.chart_options.add_widget(self.bollinger_bands_check)
        self.trend_indicator_check = QCheckBox("Trend Indicator")
        self.trend_indicator_check.clicked.connect(self.trend_indicator_check_checkchanged)
        self.chart_options.add_widget(self.trend_indicator_check)
        self.chart_options.setFixedHeight(20)
        self.add_widget(self.chart_options)

        self.add_widget(self.chart)

    def submit_event(self):
        self.chart.refresh_data()

    def trend_indicator_check_checkchanged(self):
        self.chart.trend_indicator_check_checkchanged(self.trend_indicator_check.isChecked())

    def draw_bollinger_bands(self):
        self.chart.draw_bollinger_bands(self.bollinger_bands_check.isChecked())

    def find_local_mins_and_maxes(self):
        can: Candle
        prev_can: Candle
        next_can: Candle
        for i in range(1, len(self.candles) - 1):
            prev_can = self.candles[i - 1]
            can = self.candles[i]
            next_can = self.candles[i + 1]
            if can.sma < prev_can.sma and can.sma < next_can.sma:
                can.local_min = True
            if can.sma > prev_can.sma and can.sma > next_can.sma:
                can.local_max = True

    def detect_trends(self):
        self.find_local_mins_and_maxes()

    def strategy_run_event(self, account: Account):
        self.chart.strategy_run_event(account)

    def clear_chart(self):
        self.chart.clear()



