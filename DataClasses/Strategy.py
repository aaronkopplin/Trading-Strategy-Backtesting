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
from DataClasses.Trade import Trade
from Controls.StatisticsTable import StatisticsTable
from Utilities.TextUtilities import format_as_two_decimal_price


class Strategy:
    def __init__(self):
        # private vars
        self.account: Account = None
        self.chart: ChartAndIndicator = None
        self.performance_chart: LineChart = None
        self.__statistics: StatisticsTable = None

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
        self.performance_chart = chart

    def set_statistics_table(self, table: StatisticsTable):
        self.__statistics = table

    def set_chart(self, chart: ChartAndIndicator):
        self.chart = chart

    def set_candles(self, candles: list[Candle]):
        self.candles = candles
        self.indicators = Indicators(self.candles)

    def run(self):
        self.account.store_account_value(self.candles[0].close())
        self.chart.clear_strategy()

        self._before_strategy()
        for i in range(len(self.candles)):
            self.curr_candle = self.candles[i]
            self.curr_index = i
            if i > 0:
                self.prev_candle = self.candles[i - 1]
                self.prev_index = i - 1
            self._next_candle()
            self.account.store_account_value(self.curr_candle.close())

        self.after_strategy()
        self.plot_values_on_chart()
        self.plot_indicators()
        self.chart.zoom_max()
        account_values = self.account.get_account_values()
        self.__plot_performance("PERFORMANCE",
                                account_values,
                                RGBA(255, 255, 255, 255))
        self.print_statistics()

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
    def after_strategy(self):
        pass

    # protected members
    def _set_name(self, name: str):
        self.name = name

    def _set_account_bal(self, bal: float):
        self.account = Account(bal)

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
        return (self.account.usd_balance * percent) / price

    def _buy_amount(self, amount: float, price: float = None):
        if price is None:
            price = self.curr_candle.close()
        success = self.account.buy(price, amount, self.curr_index)

    def buy_percent(self, percent: float, price: float = None):
        if price is None:
            price = self.curr_candle.close()
        cash = percent * self.account.usd_balance
        self.buy(price, cash, self.curr_index)

    def buy(self, price: float, cash: float, index: int):
        success = self.account.buy(price, cash, index)
        if success:
            self.chart.add_label(price, index, "BUY", True)

    def sell_all_open_positions(self, price: float = None):
        if price is None:
            price = self.curr_candle.close()
        success = self.account.sell_all_open_positions(price, self.curr_index)
        if success:
            self.chart.add_label(price, self.curr_index, "SELL", False)

    # private members
    def plot_values_on_chart(self):
        for collection in self.plot_values.values():
            self.chart.add_collection(collection.title, collection, collection.color)

    def plot_indicators(self):
        for i in range(len(self.plot_indicator_values)):
            item = self.plot_indicator_values[i]
            for val in item.values():
                self.chart.add_indicator(val.title, val, val.color, i)

    def __plot_performance(self, title: str, data: list[float], rgba: RGBA):
        self.performance_chart.clear_datasets()
        self.performance_chart.add_collection(title, data, rgba)
        self.performance_chart.reset_indexes()
        self.performance_chart.zoom_out_max()

    def net_profit(self):
        return round(sum(self.account.profits), 2)

    def winning_trades(self) -> list[Trade]:
        return [trade for trade in self.account.trades if trade.profit >= 0]

    def losing_trades(self) -> list[Trade]:
        return [trade for trade in self.account.trades if trade.profit < 0]

    def total_profits(self) -> float:
        winning = self.winning_trades()
        profit = sum([trade.profit for trade in winning])
        return round(profit, 2)

    def total_losses(self) -> float:
        losing = self.losing_trades()
        losses = sum([trade.profit for trade in losing])
        return round(losses, 2)

    def average_win(self):
        return round(self.total_profits() / len(self.winning_trades()), 2)

    def average_loss(self):
        return round(self.total_losses() / len(self.losing_trades()), 2)

    def portfolio_max_value(self):
        values = self.account.get_account_values()
        return max(values)

    def portfolio_min_value(self):
        values = self.account.get_account_values()
        return min(values)

    def portfolio_value(self):
        values = self.account.get_account_values()
        if len(values) > 0:
            return values[-1]
        return self.account.usd_balance

    def print_statistics(self):
        if self.__statistics:
            self.__statistics.set_column_headers("Statistic", "Output")
            self.__statistics.remove_all_rows()
            self.__statistics.add_row("Net Profits", format_as_two_decimal_price(self.net_profit()))
            self.__statistics.add_row("Total Profit", format_as_two_decimal_price(self.total_profits()))
            self.__statistics.add_row("Total Losses", format_as_two_decimal_price(self.total_losses()))
            self.__statistics.add_row("Num Buys", len(self.account.trades))
            self.__statistics.add_row("Winning Trades", len(self.winning_trades()))
            self.__statistics.add_row("Average Win", format_as_two_decimal_price(self.average_win()))
            self.__statistics.add_row("Losing Trades", len(self.losing_trades()))
            self.__statistics.add_row("Average Loss", format_as_two_decimal_price(self.average_loss()))
            self.__statistics.add_row("Portfolio max value", format_as_two_decimal_price(self.portfolio_max_value()))
            self.__statistics.add_row("Portfolio min value", format_as_two_decimal_price(self.portfolio_min_value()))
            self.__statistics.add_row("Portfolio ending value", format_as_two_decimal_price(self.portfolio_value()))
