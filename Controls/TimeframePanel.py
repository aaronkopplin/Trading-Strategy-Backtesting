import csv
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from datetime import date, timedelta
from datetime import datetime
from Controls.Button import Button
import yfinance as yf, pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
from Controls.Panel import Panel
from Controls.LayoutDirection import LayoutDirection
from Controls.TextInputWithLabel import TextInputWithLabel
from enum import Enum
from datetime import datetime
from datetime import timedelta
from Controls.ComboBox import ComboBox


class TimeInterval(Enum):
    ONE_MIN = "1m"
    TWO_MIN = "2m"
    FIVE_MIN = "5m"
    FIFTEEN_MIN = "15m"
    THIRTY_MIN = "30m"
    SIXTY_MIN = "60m"
    NINETY_MIN = "90m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"
    FIVE_DAY = "5d"
    ONE_WK = "1wk"
    ONE_MONTH = "1mo"
    THREE_MONTH = "3mo"


class Period(Enum):
    ONE_DAY = "1d"
    FIVE_DAYS = "5d"
    ONE_MONTH = "1mo"
    THREE_MONTH = "3mo"
    SIX_MONTH = "6mo"
    ONE_YEAR = "1y"
    TWO_YEAR = "2y"
    FIVE_YEAR = "5y"
    TEN_YEAR = "10y"
    YTD = "ytd"
    MAX = "max"


class TimeframePanel(Panel):
    def __init__(self):
        super().__init__()
        self.set_layout(LayoutDirection.HORIZONTAL)

        #  interval selector
        self.interval_selector = ComboBox()
        self.interval_selector.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.interval_selector.addItem(TimeInterval.ONE_MIN.value)
        self.interval_selector.addItem(TimeInterval.TWO_MIN.value)
        self.interval_selector.addItem(TimeInterval.FIVE_MIN.value)
        self.interval_selector.addItem(TimeInterval.FIFTEEN_MIN.value)
        self.interval_selector.addItem(TimeInterval.THIRTY_MIN.value)
        self.interval_selector.addItem(TimeInterval.SIXTY_MIN.value)
        self.interval_selector.addItem(TimeInterval.NINETY_MIN.value)
        self.interval_selector.addItem(TimeInterval.ONE_HOUR.value)
        self.interval_selector.addItem(TimeInterval.ONE_DAY.value)
        self.interval_selector.addItem(TimeInterval.FIVE_DAY.value)
        self.interval_selector.addItem(TimeInterval.ONE_WK.value)
        self.interval_selector.addItem(TimeInterval.ONE_MONTH.value)
        self.interval_selector.addItem(TimeInterval.THREE_MONTH.value)
        self.interval_selector.setCurrentText(TimeInterval.ONE_DAY.value)
        self.interval_selector.currentTextChanged.connect(self.selector_text_changed_event)
        self.add_widget(self.interval_selector)

        # period selector
        self.period_selector = ComboBox()
        self.period_selector.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.period_selector.addItem(Period.ONE_DAY.value)
        self.period_selector.addItem(Period.FIVE_DAYS.value)
        self.period_selector.addItem(Period.ONE_MONTH.value)
        self.period_selector.addItem(Period.THREE_MONTH.value)
        self.period_selector.addItem(Period.SIX_MONTH.value)
        self.period_selector.addItem(Period.ONE_YEAR.value)
        self.period_selector.addItem(Period.TWO_YEAR.value)
        self.period_selector.addItem(Period.FIVE_YEAR.value)
        self.period_selector.addItem(Period.TEN_YEAR.value)
        self.period_selector.addItem(Period.YTD.value)
        self.period_selector.addItem(Period.MAX.value)
        self.period_selector.setCurrentText(Period.TWO_YEAR.value)
        self.period_selector.currentTextChanged.connect(self.selector_text_changed_event)
        self.add_widget(self.period_selector)

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

        self.submit_event = None
        self.ticker_symbol = ""

    def period_invalid(self):
        return (self.interval_selector.currentText() == TimeInterval.ONE_MIN.value or
                self.interval_selector.currentText() == TimeInterval.TWO_MIN.value or
                self.interval_selector.currentText() == TimeInterval.FIVE_MIN.value or
                self.interval_selector.currentText() == TimeInterval.FIFTEEN_MIN.value or
                self.interval_selector.currentText() == TimeInterval.THIRTY_MIN.value or
                self.interval_selector.currentText() == TimeInterval.SIXTY_MIN.value or
                self.interval_selector.currentText() == TimeInterval.NINETY_MIN.value or
                self.interval_selector.currentText() == TimeInterval.ONE_HOUR.value) and not \
                (self.period_selector.currentText() == Period.ONE_DAY.value or
                 self.period_selector.currentText() == Period.FIVE_DAYS.value or
                 self.period_selector.currentText() == Period.ONE_MONTH.value)

    def selector_text_changed_event(self):
        self.submit_button.setEnabled(not self.period_invalid())

    def run_query(self):
        interval = self.interval_selector.currentText()
        ticker = self.ticker_symbol_edit.get_text()
        period = self.period_selector.currentText()

        tick = yf.Ticker(str(ticker))
        hist_data = tick.history(period=period, interval=interval)
        mom_data = add_all_ta_features(hist_data, open="Open", high="High", low="Low", close="Close", volume="Volume")

        if self.submit_event is not None:
            self.submit_event(mom_data)
