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
        self.fee_percent = .001
        self.fees_taken = 0

    def store_account_value(self, price: float):
        value = self.account_value(price)
        self.account_values.append(value)
        self.cash_reserve_values.append(self.usd_balance)

    def account_value(self, price: float):
        return self.usd_balance + (price * self.crypto_balance)

    def take_fee(self, fee: float):
        self.fees_taken += fee
        self.usd_balance -= fee

    def buy(self, price: float, amount: float, candle_index: int) -> bool:
        fee = amount * self.fee_percent
        if amount + fee < self.usd_balance:
            trade = Trade(price, amount, candle_index, self.usd_balance - amount)
            self.trades.append(trade)
            self.crypto_balance += trade.crypto_amount
            self.usd_balance -= trade.usd_amount
            self.take_fee(fee)
            return True
        return False

    def sell(self, price: float, index: int, candle_index: int):
        trade = self.trades[index]
        amt = trade.crypto_amount * price
        fee = amt * self.fee_percent
        if fee < self.usd_balance:
            profit, amount_returned = trade.sell(price, candle_index)
            self.usd_balance += amount_returned + profit
            self.take_fee(fee)
            self.crypto_balance -= trade.crypto_amount
            self.profits.append(profit)
            return True
        return False

    def sell_all_open_positions(self, price: float, candle_index: int) -> bool:
        success = False
        for i in range(len(self.trades)):
            if self.trades[i].open:
                if self.sell(price, i, candle_index):
                    success = True
        return success

