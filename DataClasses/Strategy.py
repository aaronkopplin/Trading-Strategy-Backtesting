import typing
from PyQt5.QtWidgets import *
from DataClasses.Candle import Candle
from DataClasses.Account import Account
from Controls.ChartAndIndicator import ChartAndIndicator
from DataClasses.RGBA import RGBA
from Controls.InfoPanel import InfoPanel
from DataClasses.Collection import Collection
from Controls.LineChart import LineChart
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Indicators.BollingerBands import bollinger_bands


class Strategy:
    def __init__(self):
        self.__account: Account = None
        self.__chart: ChartAndIndicator = None
        self.__plot_values: typing.Dict[str, Collection] = {}
        self.__plot_indicator_values: list[typing.Dict[str, Collection]] = []
        self.__curr_candle_index = 0
        self.__performance_chart: LineChart = None
        self._statistics: QTableView = None
        self._name = None
        self._prev_candle: Candle = None
        self._curr_candle: Candle = None
        self._candles = None

    # public members
    def set_performance_chart(self, chart: LineChart):
        self.__performance_chart = chart

    def set_statistics_table(self, table: QTableView):
        self._statistics = table

    def set_chart(self, chart: ChartAndIndicator):
        self.__chart = chart

    def set_candles(self, candles: list[Candle]):
        self._candles = candles

    def run(self):
        self.__account.store_account_value(self._candles[0].close())

        for i in range(len(self._candles)):
            self._curr_candle = self._candles[i]
            if i > 0:
                self._prev_candle = self._candles[i - 1]
            self.__curr_candle_index = i
            self._next_candle()
            self.__account.store_account_value(self._curr_candle.close())

        self.__chart.clear_strategy()
        self.__plot_values_on_chart()
        self.__plot_indicators()
        self.__chart.zoom_max()
        account_values = self.__account.get_account_values()
        self.__plot_performance("PERFORMANCE",
                                account_values,
                                RGBA(255, 255, 255, 255))
        self._print_statistics()

    # protected members
    def _set_name(self, name: str):
        self._name = name

    def _set_account_bal(self, bal: float):
        self.__account = Account(bal)

    def plot(self, title: str, data: float, rgba: RGBA):
        if self.__plot_values.get(title) is None:
            self.__plot_values[title] = Collection(title, [], rgba)
        data_values: Collection = self.__plot_values[title]
        data_values.append(data)

    def plot_indicator(self, title: str, data: float, rgba: RGBA, index: int):
        if index >= len(self.__plot_indicator_values):
            self.__plot_indicator_values.append({title: Collection(title, [data], rgba)})
        else:
            self.__plot_indicator_values[index][title].append(data)

    def _get_amount_for_percent(self, percent: float, price: float = None):
        if price is None:
            price = self._curr_candle.close()

        if percent < 0 or percent > 100:
            raise ValueError("Percent cannot be less than zero or greater than 100")
        return (self.__account.usd_balance * percent) / price

    def _buy_amount(self, amount: float, price: float = None):
        if price is None:
            price = self._curr_candle.close()
        self.__account.buy(price, amount, self.__curr_candle_index)

    def buy_percent(self, percent: float, price: float = None):
        if price is None:
            price = self._curr_candle.close()
        cash = percent * self.__account.usd_balance
        self.__account.buy(price, cash, self.__curr_candle_index)

    def _sell(self):
        pass

    def _next_candle(self):
        pass

    # private members
    def __plot_values_on_chart(self):
        for collection in self.__plot_values.values():
            self.__chart.add_collection(collection.title, collection, collection.color)

    def __plot_indicators(self):
        for i in range(len(self.__plot_indicator_values)):
            item = self.__plot_indicator_values[i]
            for val in item.values():
                self.__chart.add_indicator(val.title, val, val.color, i)

    def __plot_performance(self, title: str, data: list[float], rgba: RGBA):
        self.__performance_chart.add_collection(title, data, rgba)
        self.__performance_chart.zoom_out_max()

    def net_profit(self):
        return sum(self.__account.profits)

    def _print_statistics(self):
        if self._statistics:
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(["Statistic", "Output"])
            model.setItem(0, 0, QStandardItem("Net Profits"))
            model.setItem(0, 1, QStandardItem(str(self.net_profit())))
            self._statistics.setModel(model)
