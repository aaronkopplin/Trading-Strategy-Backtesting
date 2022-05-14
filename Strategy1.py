from DataClasses.Strategy import Strategy
from Controls.ChartAndIndicator import ChartAndIndicator
from overrides import overrides
from DataClasses.Candle import Candle
from DataClasses.RGBA import RGBA
from Utilities.MovingAverages import moving_average


class Strategy1(Strategy):
    def __init__(self, chart: ChartAndIndicator, candles: list[Candle]):
        super().__init__("Bollinger Bands Breakout", 1000, chart, candles)

    @overrides
    def run(self, candles: list[Candle]):
        closes = []
        for i in range(len(candles)):
            can = candles[i]
            closes.append(can.close())

        self.plot(moving_average(closes, time_period=10), RGBA(255, 0, 255, 255))
        self.plot(moving_average(closes, time_period=50), RGBA(0, 0, 255, 255))

        self.plot_indicator(closes, RGBA(0, 255, 0, 255))