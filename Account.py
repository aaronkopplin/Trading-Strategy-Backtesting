from Candle import Candle


class Account:
    def __init__(self, balance: float):
        self.usd_balance = balance
        self.btc_balance = 0

    def buy(self, amount: float, candle: Candle):
        self.btc_balance += amount / candle.open
        self.usd_balance -= amount

    def sell(self, amount: float, candle: Candle):
        self.btc_balance -= amount / candle.open
        self.usd_balance += amount


