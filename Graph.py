import csv
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import date, timedelta
from datetime import datetime
from Chart import Chart
from Strategy import Account, Trade


class Graph(QtWidgets.QWidget):
    def __init__(self, candles: list):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.chart = Chart(candles)
        self.layout.addWidget(self.chart)
        self.setLayout(self.layout)

        # row one
        # self.row_one_panel = QWidget()
        # self.layout.addWidget(self.row_one_panel)
        # self.row_one_panel_layout = QHBoxLayout()
        # self.row_one_panel_layout.setContentsMargins(0, 0, 0, 0)
        # self.row_one_panel.setLayout(self.row_one_panel_layout)
        # self.row_one_panel.setFixedHeight(50)

        # row two
        self.row_two_panel = QWidget()
        self.layout.addWidget(self.row_two_panel)
        self.row_two_panel_layout = QHBoxLayout()
        self.row_two_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.row_two_panel.setLayout(self.row_two_panel_layout)
        self.row_two_panel.setFixedHeight(50)

        # begin time frame
        self.begin_timeframe = QDateTimeEdit()
        self.begin_timeframe.setDateTime(QDateTime(date.today() - timedelta(7)))
        self.row_two_panel_layout.addWidget(self.begin_timeframe)

        # end time frame
        self.end_timeframe = QDateTimeEdit()
        self.end_timeframe.setDateTime(QDateTime(date.today()))
        self.row_two_panel_layout.addWidget(self.end_timeframe)

        #  candle selector
        self.candle_selector = QComboBox()
        self.candle_selector.addItem("1m")
        self.candle_selector.addItem("2m")
        self.candle_selector.addItem("5m")
        self.candle_selector.addItem("15m")
        self.candle_selector.addItem("30m")
        self.candle_selector.addItem("1h")
        self.candle_selector.addItem("1d")
        self.candle_selector.addItem("5d")
        self.candle_selector.addItem("1wk")
        self.row_two_panel_layout.addWidget(self.candle_selector)

        # load parameters
        self.load_parameters()

        # submit_button button
        self.submit_button = QPushButton("submit")
        self.submit_button.clicked.connect(self.run_query)
        self.row_two_panel_layout.addWidget(self.submit_button)

    def strategy_run_event(self, account: Account):
        self.chart.strategy_run_event(account)


    def load_parameters(self):
        data = []
        with open("last_query.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        parameters = data.pop()
        ticker = parameters[0]
        begin = parameters[1]
        end = parameters[2]
        interval = parameters[3]

        self.begin_timeframe.setDateTime(datetime.strptime(begin, "%Y-%m-%d"))
        self.end_timeframe.setDateTime(datetime.strptime(end, "%Y-%m-%d"))
        self.candle_selector.setCurrentText(interval)

    def run_query(self):
        self.chart.run_query(self.begin_timeframe.dateTime(),
                             self.end_timeframe.dateTime(),
                             self.candle_selector.currentText())


