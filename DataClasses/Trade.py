from typing import Union


class Trade:
    def __init__(self, buy_price: float, amount: float, candle_index: int, usd_acct_bal):
        self.buy_price = buy_price
        self.sell_price: float = 0.0
        self.profit: float = 0.0
        self.usd_amount = amount
        self.crypto_amount = amount / buy_price
        self.open: bool = True
        self.buy_candle_index = candle_index
        self.sell_candle_index: Union[int, None] = None
        self.account_usd_bal = usd_acct_bal

    def sell(self, sell_price: float, candle_index: int) -> tuple[float, float]:
        self.open = False
        self.sell_price = sell_price
        self.profit = self.crypto_amount * (self.sell_price - self.buy_price)
        self.sell_candle_index = candle_index
        return self.profit, self.usd_amount
