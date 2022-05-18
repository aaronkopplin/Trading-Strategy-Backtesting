from DataClasses.Candle import Candle
from DataClasses.Account import Account
from Controls.ChartAndIndicator import ChartAndIndicator
from DataClasses.RGBA import RGBA
from Controls.InfoPanel import InfoPanel
from DataClasses.Collection import Collection


class Strategy:
    def __init__(self):
        self.__account: Account = None
        self.__chart: ChartAndIndicator = None
        self.__plot_values = {}
        self.__curr_candle_index = 0
        self.__performance_chart: InfoPanel = None
        self._name = None
        self._prev_candle: Candle = None
        self._curr_candle: Candle = None
        self._candles = None

    def set_performance_chart(self, chart: InfoPanel):
        self.__performance_chart = chart

    def _set_name(self, name: str):
        self._name = name

    def _set_account_bal(self, bal: float):
        self.__account = Account(bal)

    def set_chart(self, chart: ChartAndIndicator):
        self.__chart = chart

    def set_candles(self, candles: list[Candle]):
        self._candles = candles

    def _plot(self, title: str, data: float, rgba: RGBA):
        if self.__plot_values.get(title) is None:
            self.__plot_values[title] = Collection(title, [], rgba)
        data_values: Collection = self.__plot_values[title]
        data_values.append(data)

    def __plot(self):
        self.__chart.clear_strategy()
        for collection in self.__plot_values.values():
            self.__chart.add_collection(collection.title, collection, collection.color)

    def __plot_indicator(self, title: str, data: list[float], rgba: RGBA):
        self.__chart.add_indicator(title, data, rgba)

    def __plot_performance(self, title: str, data: list[float], rgba: RGBA):
        self.__performance_chart.add_collection(title, data, rgba)

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
        pass

    def _sell(self):
        pass

    def run(self):
        self.__account.store_account_value(self._candles[0].close())

        for i in range(len(self._candles)):
            self._curr_candle = self._candles[i]
            if i > 0:
                self._prev_candle = self._candles[i - 1]
            self.__curr_candle_index = i
            self._next_candle()
            self.__account.store_account_value(self._curr_candle.close())
        self.__plot()
        self.__performance_chart.add_collection("PERFORMANCE",
                                                self.__account.get_account_values(),
                                                RGBA(255, 255, 255, 255))

    def _next_candle(self):
        pass

