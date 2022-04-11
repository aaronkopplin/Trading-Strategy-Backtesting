import csv
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import date, timedelta
from datetime import datetime

import StyleInfo
from Chart import Chart
from Strategy import Account, Trade
from TimeframePanel import TimeframePanel
from Controls.Panel import Panel
from Controls.LayoutDirection import LayoutDirection
from Controls.Splitter import Splitter


class Graph(Panel):
    def __init__(self, candles: list):
        super().__init__()
        self.splitter = Splitter(LayoutDirection.VERTICAL)
        self.add_widget(self.splitter)

        self.chart = Chart(candles)
        self.splitter.addWidget(self.chart)

        self.timeframe_panel = TimeframePanel(self.chart)
        self.splitter.addWidget(self.timeframe_panel)

    def strategy_run_event(self, account: Account):
        self.chart.strategy_run_event(account)

    def clear_chart(self):
        self.chart.clear()



