from typing import Callable
from Account import Account
from Strategy import Strategy
from Candle import Candle
from Trade import Trade


def strategy_1(parameters: dict, callback: Callable):
    candles = parameters["candles"]
    account = Account(1000)
    percent_per_trade = .05
    breakout = False
    first_trade_after_sell = None
    price_at_sell = 0
    for i in range(2, len(candles)):
        trade_decision = ""
        prev_can = candles[i-1]
        can: Candle = candles[i]
        if can.open < can.lower_band and can.close < can.lower_band:
            trade_decision = "Buy"
        if can.close > can.upper_band:
            breakout = True
        if breakout and can.close < can.sma:
            breakout = False
            trade_decision = "Sell"
            price_at_sell = can.sma

        # stop loss
        if len(account.trades) > 0 and first_trade_after_sell is not None:
            if can.close < (first_trade_after_sell.buy_price * .995):
                trade_decision = "Sell"
                price_at_sell = can.close

        if trade_decision == "Buy":
            amount = account.usd_balance * percent_per_trade
            account.buy(can.close, amount, i)
            can.set_bought_price(can.close)
            if percent_per_trade < .1:
                percent_per_trade += .00
            if first_trade_after_sell is None:
                first_trade_after_sell = account.trades[-1]
        elif trade_decision == "Sell":
            success = account.sell_all_open_positions(price_at_sell, i)
            percent_per_trade = .05
            first_trade_after_sell = None
            if success:
                can.set_sell_price(price_at_sell)

        account.store_account_value(can.close)

    callback(account)


def buy_low_sell_mid(parameters: dict, callback: Callable):
    candles = parameters["candles"]

    account = Account(1000)
    percent_per_trade = .05
    first_trade_after_sell = None
    for i in range(2, len(candles)):
        trade_decision = ""
        can = candles[i]
        # prev_can = candles[i-1]

        if can.close < can.lower_band:
            trade_decision = "Buy"
        if can.close > can.upper_band:
            trade_decision = "Sell"

        # stop loss
        if len(account.trades) > 0 and first_trade_after_sell is not None:
            if can.close < (first_trade_after_sell.buy_price * .99):
                trade_decision = "Sell"

        # execute trade decision
        if trade_decision == "Buy":
            amount = account.usd_balance * percent_per_trade
            account.buy(can.close, amount, i)
            if first_trade_after_sell is None:
                first_trade_after_sell = account.trades[-1]
            if percent_per_trade < .1:
                percent_per_trade += .01
        elif trade_decision == "Sell":
            account.sell_all_open_positions(can.close, i)
            first_trade_after_sell = None
            percent_per_trade = .05

        account.store_account_value(can.close)
    callback(account)


def buy_low_sell_mid_shrinking(parameters: dict, callback: Callable):
    candles = parameters["candles"]

    account = Account(1000)
    percent_per_trade = .05
    breakout = False
    for i in range(2, len(candles)):
        can = candles[i]
        prev_can = candles[i-1]

        if can.close < can.lower_band:
            amount = account.usd_balance * percent_per_trade
            account.buy(can.close, amount, i)
            if percent_per_trade < .1:
                percent_per_trade += .01
        if can.close > can.sma:
            account.sell_all_open_positions(prev_can.sma, i)
            percent_per_trade = .05
        account.store_account_value(can.close)
    callback(account)



strategies = [
    Strategy("BUY LOW, BREAKOUT, SELL MID", strategy_1),
    # Strategy("BUY LOWER BAND SELL UPPER BAND, STOPLOSS 1%", buy_low_sell_mid),
    # Strategy("BUY LOW SELL MID SHRINKING", buy_low_sell_mid_shrinking),
]
