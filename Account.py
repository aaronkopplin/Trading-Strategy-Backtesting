from Trade import Trade


class Account:
    def __init__(self, balance: float):
        self.beginning_balance = balance
        self.usd_balance: float = balance
        self.crypto_balance: float = 0
        self.trades: list[Trade] = []
        self.account_values = []
        self.cash_reserve_values = []
        self.profits = []

    def store_account_value(self, price: float):
        value = self.account_value(price)
        self.account_values.append(value)
        self.cash_reserve_values.append(self.usd_balance)

    def account_value(self, price: float):
        return self.usd_balance + (price * self.crypto_balance)

    def buy(self, price: float, amount: float, candle_index: int):
        if amount < self.usd_balance:
            trade = Trade(price, amount, candle_index, self.usd_balance - amount)
            self.trades.append(trade)
            self.crypto_balance += trade.crypto_amount
            self.usd_balance -= trade.usd_amount

    def sell(self, price: float, index: int, candle_index: int):
        profit = self.trades[index].sell(price, candle_index)
        self.usd_balance += self.trades[index].usd_amount
        self.usd_balance += profit
        self.crypto_balance -= self.trades[index].crypto_amount
        self.profits.append(profit)

    def sell_all_open_positions(self, price: float, candle_index: int):
        for i in range(len(self.trades)):
            if self.trades[i].open:
                self.sell(price, i, candle_index)

