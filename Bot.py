import csv
from Candle import Candle
from Account import Account
from Bollinger import *
from Gui import open_application


results = []
candles = []
with open("data.csv") as file:
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


print("percent gain for timeframe", ((candles[len(candles) - 1].open - candles[0].open ) / candles[0].open) * 100)

open_application(candles)

# account = Account(100)
# prev_candle = candles.pop()
# account.buy(account.usd_balance * .5, prev_candle)
# for can in candles:
#     next_candle = candles.pop()
#     if