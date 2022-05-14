import csv
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import date, timedelta
from datetime import datetime
from Controls.CandleChart import CandleChart
from Controls.Button import Button
import yfinance
from Controls.Panel import Panel
from Controls.LayoutDirection import LayoutDirection
from Controls.TextInputWithLabel import TextInputWithLabel


class TimeframePanel(Panel):
    def __init__(self):
        super().__init__()
        self.set_layout(LayoutDirection.HORIZONTAL)

        # begin time frame
        self.begin_timeframe = QDateTimeEdit()
        self.begin_timeframe.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.begin_timeframe.setDateTime(QDateTime(date.today() - timedelta(7)))
        self.add_widget(self.begin_timeframe)

        # end time frame
        self.end_timeframe = QDateTimeEdit()
        self.end_timeframe.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.end_timeframe.setDateTime(QDateTime(date.today()))
        self.add_widget(self.end_timeframe)

        #  candle selector
        self.candle_selector = QComboBox()
        self.candle_selector.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.candle_selector.addItem("1m")
        self.candle_selector.addItem("2m")
        self.candle_selector.addItem("5m")
        self.candle_selector.addItem("15m")
        self.candle_selector.addItem("30m")
        self.candle_selector.addItem("1h")
        self.candle_selector.addItem("1d")
        self.candle_selector.addItem("5d")
        self.candle_selector.addItem("1wk")
        self.add_widget(self.candle_selector)

        # ticker symbol
        self.ticker_symbol_edit: TextInputWithLabel = TextInputWithLabel("TICKER: ")
        self.ticker_symbol_edit.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.ticker_symbol_edit.setFixedWidth(200)
        self.ticker_symbol_edit.text_input.setText("BTC-USD")
        self.add_widget(self.ticker_symbol_edit)

        # submit_button button
        self.submit_button = Button()
        self.submit_button.setText("SUBMIT")
        self.submit_button.clicked.connect(self.run_query)
        self.add_widget(self.submit_button)

        self.load_parameters()

        self.submit_event = None

    def run_query(self):
        begin = self.begin_timeframe.dateTime()
        end = self.end_timeframe.dateTime()
        interval = self.candle_selector.currentText()
        ticker = self.ticker_symbol_edit.get_text()

        start = f"{begin.date().year()}-{begin.date().month()}-{begin.date().day()}"
        end = f"{end.date().year()}-{end.date().month()}-{end.date().day()}"
        data = yfinance.download([ticker],
                                 start=start,
                                 end=end,
                                 interval=interval)

        if len(data) > 1:
            data.to_csv("Data/data.csv")
            with open("./Data/last_query.csv", "w") as f:
                f.write("ticker_symbol,begin,end,interval\n")
                f.write(f"{ticker},{start},{end},{interval}")

        if self.submit_event is not None:
            self.submit_event()

    def load_parameters(self):
        data = []
        with open("./Data/last_query.csv") as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        parameters = data.pop()
        ticker = parameters[0]
        begin = parameters[1]
        end = parameters[2]
        interval = parameters[3]

        self.ticker_symbol_edit.set_text(ticker)
        self.begin_timeframe.setDateTime(datetime.strptime(begin, "%Y-%m-%d"))
        self.end_timeframe.setDateTime(datetime.strptime(end, "%Y-%m-%d"))
        self.candle_selector.setCurrentText(interval)