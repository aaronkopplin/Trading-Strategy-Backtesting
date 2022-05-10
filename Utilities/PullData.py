import csv
from DataClasses.Candle import Candle
from Utilities.Bollinger import *

#
# data = yfinance.download(["BTC-USD"], start="2021-11-11", end="2021-11-18", interval="1h")
# data.to_csv("data.csv")


def read_candles():
    results = []
    candles = []
    with open("./Data/data.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            results.append(row)

    results = results[1:len(results)]
    for result in results:
        candles.append(Candle(result))

    for i in range(2, len(candles)):
        first = 0
        if i > bollinger_period:
            first = i - bollinger_period
        last = i
        period_candles = candles[first:last]
        candles[i].sma, candles[i].upper_band, candles[i].lower_band = bollinger_bands(period_candles)

    return candles
