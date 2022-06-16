# Trading Strategy Backtesting  
![image](https://user-images.githubusercontent.com/48528737/174193338-97166785-a926-4a0e-97db-77a8403130f3.png)

This program allows you to plot stock or crypto data, create your own technical indicators, and backtest trading strategies

To create a strategy, inherit from "Strategy.py". There is an exmaple strategy in "Strategy1.py"

Run your strategy with Ctrl + R

The rest should be pretty self explanatory.

# Running the program
~ install the dependencies ~   
cd C:\path\to\directory  
`python Bot.py`

# Dependencies: 

PyQt5: https://pypi.org/project/PyQt5/. `pip install PyQt5`

yfinance: https://pypi.org/project/yfinance/.  `pip install yfinance`

Overrides: https://pypi.org/project/overrides/.  `pip install overrides`

ta: https://github.com/bukosabino/ta.  `pip install --upgrade ta`  
  
# Example strategy

```
class Strategy1(Strategy):
    def __init__(self):
        super().__init__()
        self._set_name("First strategy")
        self._set_account_bal(1000)

        # user defined plot values
        self.highs = Collection("HIGHS", [], RGBA(255, 255, 255, 255))
        self.lower_band = Collection("LOWER", [], RGBA(255, 0, 0, 255))
        self.middle_band = Collection("MIDDLE", [], RGBA(0, 255, 0, 255))
        self.upper_band = Collection("UPPER", [], RGBA(0, 0, 255, 255))
        self.slow_sma = Collection("SMA 200", [], RGBA(255, 255, 0, 255))

        # plot performance
        self.values = Collection("PORTFOLIO", [], RGBA(0, 255, 0, 255))

    @overrides
    def _before_strategy(self):
        pass

    @overrides
    def _next_candle(self):
        bb_length = 20
        bb_stdev = 2
        slow_sma_length = 200

        self.highs.append(self.curr_candle.high())

        # built in bollinger band indicator. adding more indicators in the future
        lower, middle, upper = self.indicators.bollinger_bands(self.curr_index, bb_length, bb_stdev)
        self.lower_band.append(lower)
        self.middle_band.append(middle)
        self.upper_band.append(upper)

        self.values.append(self.account.account_value(self.curr_candle.close()))

        slow_sma = self.indicators.sma_closes(self.curr_index, slow_sma_length)
        self.slow_sma.append(slow_sma)

        if self.prev_candle and self.curr_index > slow_sma_length:
            prev_lower, prev_middle, prev_upper = self.indicators.bollinger_bands(self.prev_index, bb_length, bb_stdev)
            prev_slow_sma = self.indicators.sma_closes(self.prev_index, slow_sma_length)

            bear_cross_up = self.prev_candle.close() < prev_lower and self.curr_candle.close() > lower
            bear_cross_down = self.prev_candle.close() < prev_slow_sma and self.curr_candle.close() > slow_sma

            # buy and sell
            if middle < slow_sma:
                if bear_cross_up:
                    self.buy_percent(.05)
            if middle > slow_sma:
                if bear_cross_down:
                    self.sell_all_open_positions()

    @overrides
    def after_strategy(self):
        # plot values appear on the candle chart
        self.add_plot_value("LOWER", self.lower_band)
        self.add_plot_value("MIDDLE", self.middle_band)
        self.add_plot_value("UPPER", self.upper_band)
        self.add_plot_value("SMA 200", self.slow_sma)

        # indicators appear below the main candle chart
        self.add_indicator_value("HIGHS", self.highs, 0)
        self.add_indicator_value("PORTFOLIO", self.values, 1)

```
