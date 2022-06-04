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
from Indicator.Indicators import Indicators


class Strategy:
    def __init__(self):

        # private vars
        self.__account: Account = None
        self.__chart: ChartAndIndicator = None
        self.__performance_chart: LineChart = None
        self.__statistics: QTableView = None

        # public vars
        self.plot_values: typing.Dict[str, Collection] = {}
        self.plot_indicator_values: list[typing.Dict[str, Collection]] = []
        self.curr_index = 0
        self.prev_index = 0
        self.name = None
        self.prev_candle: Candle = None
        self.curr_candle: Candle = None
        self.candles: list[Candle] = None
        self.indicators: Indicators = None

    # public members
    def set_performance_chart(self, chart: LineChart):
        self.__performance_chart = chart

    def set_statistics_table(self, table: QTableView):
        self.__statistics = table

    def set_chart(self, chart: ChartAndIndicator):
        self.__chart = chart

    def set_candles(self, candles: list[Candle]):
        self.candles = candles
        self.indicators = Indicators(self.candles)

    def run(self):
        self.__account.store_account_value(self.candles[0].close())

        self._before_strategy()
        for i in range(len(self.candles)):
            self.curr_candle = self.candles[i]
            if i > 0:
                self.prev_candle = self.candles[i - 1]
                self.prev_index = i - 1
            self._next_candle()
            self.curr_index = i
            self.__account.store_account_value(self.curr_candle.close())

        self._after_strategy()
        self.__chart.clear_strategy()
        self.__plot_values_on_chart()
        self.__plot_indicators()
        self.__chart.zoom_max()
        account_values = self.__account.get_account_values()
        self.__plot_performance("PERFORMANCE",
                                account_values,
                                RGBA(255, 255, 255, 255))
        self._print_statistics()

    # call in child class to plot on main candle chart
    def add_plot_value(self, title: str, data: Collection):
        if len(data) == 0:
            raise ValueError("Cannot add empty collection!")
        self.plot_values[title] = data

    #  call in child class to plot on indicator charts below main chart
    def add_indicator_value(self, title: str, data: Collection, index: int):
        if len(data) == 0:
            raise ValueError("Cannot add empty collection!")
        if len(self.plot_indicator_values) <= index:
            self.plot_indicator_values.append({title: data})
            return

        self.plot_indicator_values[index][title] = data

    # override in child classes
    def _next_candle(self):
        pass

    # override in child classes
    def _before_strategy(self):
        pass

    # override in child classes
    def _after_strategy(self):
        pass

    # protected members
    def _set_name(self, name: str):
        self.name = name

    def _set_account_bal(self, bal: float):
        self.__account = Account(bal)

    def plot(self, title: str, data: float, rgba: RGBA):
        if self.plot_values.get(title) is None:
            self.plot_values[title] = Collection(title, [], rgba)
        data_values: Collection = self.plot_values[title]
        data_values.append(data)

    def _get_amount_for_percent(self, percent: float, price: float = None):
        if price is None:
            price = self.curr_candle.close()

        if percent < 0 or percent > 100:
            raise ValueError("Percent cannot be less than zero or greater than 100")
        return (self.__account.usd_balance * percent) / price

    def _buy_amount(self, amount: float, price: float = None):
        if price is None:
            price = self.curr_candle.close()
        self.__account.buy(price, amount, self.curr_index)

    def buy_percent(self, percent: float, price: float = None):
        if price is None:
            price = self.curr_candle.close()
        cash = percent * self.__account.usd_balance
        self.buy(price, cash, self.curr_index)

    def buy(self, price: float, cash: float, index: int):
        success = self.__account.buy(price, cash, index)
        if success:
            self.__chart.add_label(price, index, "BUY", True)

    def sell_all_open_positions(self, price: float = None):
        if price is None:
            price = self.curr_candle.close()
        success = self.__account.sell_all_open_positions(price, self.curr_index)
        if success:
            self.__chart.add_label(price, self.curr_index, "SELL", False)

    # private members
    def __plot_values_on_chart(self):
        for collection in self.plot_values.values():
            self.__chart.add_collection(collection.title, collection, collection.color)

    def __plot_indicators(self):
        for i in range(len(self.plot_indicator_values)):
            item = self.plot_indicator_values[i]
            for val in item.values():
                self.__chart.add_indicator(val.title, val, val.color, i)

    def __plot_performance(self, title: str, data: list[float], rgba: RGBA):
        self.__performance_chart.add_collection(title, data, rgba)
        self.__performance_chart.zoom_out_max()

    def net_profit(self):
        return sum(self.__account.profits)

    def _print_statistics(self):
        if self.__statistics:
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(["Statistic", "Output"])
            model.setItem(0, 0, QStandardItem("Net Profits"))
            model.setItem(0, 1, QStandardItem(str(self.net_profit())))
            self.__statistics.setModel(model)
