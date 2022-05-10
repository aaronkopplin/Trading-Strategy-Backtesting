from DataClasses.Candle import Candle
from DataClasses.Account import Account
from Controls.LineChart import LineChart
from DataClasses.RGBA import RGBA


class Strategy:
    def __init__(self, name: str, beginning_bal: float, chart: LineChart, candles: list[Candle]):
        self.name = name
        self.account = Account(beginning_bal)
        self.chart: LineChart = chart
        self.run(candles)

    def plot(self, data: list[float], rgb: RGBA):
        self.chart.add_collection(data, rgb)

    def run(self, candles: list[Candle]):
        # loop over candles and return strategy decisions
        pass

