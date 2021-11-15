import csv
from Candle import Candle
from Account import Account
from Bollinger import *


results = []
candles = []
with open("data.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        results.append(row)

results = results[1:len(results)]
for result in results:
    candles.append(Candle(result))

for i in range(len(candles)):
    period_candles = []
    for j in range(i - bollinger_period, i):
        if j >= 0:
            period_candles.append(candles[j])

    candles[i].sma, candles[1].upper_band, candles[i].lower_band = bollinger_bands(period_candles)


print("percent gain for timeframe", ((candles[len(candles) - 1].open - candles[0].open ) / candles[0].open) * 100)

# account = Account(100)
# prev_candle = candles.pop()
# account.buy(account.usd_balance * .5, prev_candle)
# for can in candles:
#     next_candle = candles.pop()
#     if