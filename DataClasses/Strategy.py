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

    def plot(self, data: list[float], rgb: RGBA):
        self.chart.add_collection(data, rgb)

    def plot_indicator(self, data: list[float], rgba: RGBA):
        self.chart.add_indicator(data, rgba)

    def run(self, candles: list[Candle]):
        # loop over candles and make trades
        pass

