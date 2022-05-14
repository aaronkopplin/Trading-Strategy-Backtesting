from DataClasses.Candle import Candle
from DataClasses.Account import Account
from Controls.ChartAndIndicator import ChartAndIndicator
from DataClasses.RGBA import RGBA


class Strategy:
    def __init__(self, name: str, beginning_bal: float, chart: ChartAndIndicator, candles: list[Candle]):
        self.name = name
        self.account = Account(beginning_bal)
        self.chart: ChartAndIndicator = chart
        self.run(candles)

    def plot(self, title: str, data: list[float], rgb: RGBA):
        self.chart.add_collection(title, data, rgb)

    def plot_indicator(self, title: str, data: list[float], rgba: RGBA):
        self.chart.add_indicator(title, data, rgba)

    def run(self, candles: list[Candle]):
        # loop over candles and make trades
        pass

