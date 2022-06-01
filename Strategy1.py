from DataClasses.Strategy import Strategy
from Controls.ChartAndIndicator import ChartAndIndicator
from overrides import overrides
from DataClasses.Candle import Candle
from DataClasses.RGBA import RGBA
from Utilities.MovingAverages import moving_average
import random


class Strategy1(Strategy):
    def __init__(self):
        super().__init__()
        self._set_name("First strategy")
        self._set_account_bal(1000)

    @overrides
    def _next_candle(self):
        # self.
        self.buy_percent(.05)
        self.plot("CLOSES", self._curr_candle.close(), RGBA(255, 0, 255, 255))
        self.plot_indicator("HIGHS", self._curr_candle.high(), RGBA(255, 0, 255, 255), 0)
        self.plot_indicator("HIGHS", self._curr_candle.high(), RGBA(255, 0, 255, 255), 1)
        self.plot_indicator("HIGHS", self._curr_candle.high(), RGBA(255, 0, 255, 255), 2)
