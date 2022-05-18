from DataClasses.Strategy import Strategy
from Controls.ChartAndIndicator import ChartAndIndicator
from overrides import overrides
from DataClasses.Candle import Candle
from DataClasses.RGBA import RGBA
from Utilities.MovingAverages import moving_average


class Strategy1(Strategy):
    def __init__(self):
        super().__init__()
        self._set_name("First strategy")
        self._set_account_bal(1000)

    @overrides
    def _next_candle(self):
        self._buy_percent(.05)
        self._plot("TEST", self._curr_candle.close(), RGBA(0, 255, 255, 255))
