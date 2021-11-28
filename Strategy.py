from typing import Union


class Trade:
    def __init__(self, buy_price: float, amount: float, candle_index: int):
        self.buy_price = buy_price
        self.sell_price: float = 0.0
        self.profit: float = 0.0
        self.usd_amount = amount
        self.crypto_amount = amount / buy_price
        self.open: bool = True
        self.buy_candle_index = candle_index
        self.sell_candle_index: Union[int, None] = None

    def sell(self, sell_price: float, candle_index: int) -> float:
        self.open = False
        self.sell_price = sell_price
        self.profit = self.crypto_amount * (self.sell_price - self.buy_price)
        self.sell_candle_index = candle_index
        return self.profit


class Account:
    def __init__(self, balance: float):
        self.usd_balance: float = balance
        self.crypto_balance: float = 0
        self.trades: list[Trade] = []

    def account_value(self, price: float):
        print(self.usd_balance, self.crypto_balance)
        return self.usd_balance + (price * self.crypto_balance)

    def buy(self, price: float, amount: float, candle_index: int):
        if amount < self.usd_balance:
            trade = Trade(price, amount, candle_index)
            self.trades.append(trade)
            self.crypto_balance += trade.crypto_amount
            self.usd_balance -= trade.usd_amount

    def sell(self, price: float, index: int, candle_index: int):
        profit = self.trades[index].sell(price, candle_index)
        self.usd_balance += profit
        self.crypto_balance -= self.trades[index].crypto_amount

    def sell_all_open_positions(self, price: float, candle_index: int):
        i: int
        for i in range(len(self.trades)):
            if self.trades[i].open:
                self.sell(price, i, candle_index)


def strategy_1(candles: list) -> Account:
    account = Account(1000)
    breakout = False
    for i in range(2, len(candles)):
        can = candles[i]
        if can.close < can.lower_band:
            amount = account.usd_balance * .01
            account.buy(can.close, amount, i)
        if can.close > can.upper_band:
            breakout = True
        if breakout and can.open > can.sma > can.close:
            breakout = False
            account.sell_all_open_positions(can.sma, i)

    return account

