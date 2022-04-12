from typing import Callable
from Account import Account
from Strategy import Strategy


def strategy_1(parameters: dict, callback: Callable):
    candles = parameters["candles"]
    account = Account(1000)
    percent_per_trade = .05
    breakout = False
    for i in range(2, len(candles)):
        can = candles[i]
        if can.close < can.lower_band:
            amount = account.usd_balance * percent_per_trade
            account.buy(can.close, amount, i)
            if percent_per_trade < .1:
                percent_per_trade += .01
        if can.close > can.upper_band:
            breakout = True
        if breakout and can.close < can.sma:
            breakout = False
            account.sell_all_open_positions(can.sma, i)
            percent_per_trade = .01
        account.store_account_value(can.close)

    callback(account)


def buy_low_sell_mid(parameters: dict, callback: Callable):
    candles = parameters["candles"]

    account = Account(1000)
    percent_per_trade = .05
    breakout = False
    for i in range(2, len(candles)):
        can = candles[i]
        if can.close < can.lower_band:
            amount = account.usd_balance * percent_per_trade
            account.buy(can.close, amount, i)
            if percent_per_trade < .1:
                percent_per_trade += .01
        if can.close > can.sma:
            account.sell_all_open_positions(can.sma, i)
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
        if can.close < can.lower_band:
            amount = account.usd_balance * percent_per_trade
            account.buy(can.close, amount, i)
            if percent_per_trade < .1:
                percent_per_trade += .01
        if can.close > can.sma:
            account.sell_all_open_positions(can.sma, i)
            percent_per_trade = .05
        account.store_account_value(can.close)
    callback(account)



strategies = [
    Strategy("BUY LOW, BREAKOUT, SELL MID", strategy_1),
    Strategy("BUY LOW SELL MID", buy_low_sell_mid),
    Strategy("BUY LOW SELL MID SHRINKING", buy_low_sell_mid_shrinking),
]
