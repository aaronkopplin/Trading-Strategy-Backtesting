import csv
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import date, timedelta
from datetime import datetime
from Chart import Chart
from Strategy import Account, Trade
from TimeframePanel import TimeframePanel


class Graph(QtWidgets.QWidget):
    def __init__(self, candles: list):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.splitter = QSplitter(Qt.Vertical)
        self.layout.addWidget(self.splitter)

        self.chart = Chart(candles)
        self.splitter.addWidget(self.chart)

        self.timeframe_panel = TimeframePanel(self.chart)
        self.splitter.addWidget(self.timeframe_panel)

    def strategy_run_event(self, account: Account):
        self.chart.strategy_run_event(account)



