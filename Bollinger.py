from statistics import mean, stdev


bollinger_period = 20
bollinger_stdev = 2


def bollinger_bands(candles: list):
    closes = [can.close for can in candles]
    sma = mean(closes)
    upper_band = sma + (stdev(closes) * bollinger_stdev)
    lower_band = sma - (stdev(closes) * bollinger_stdev)
    return sma, upper_band, lower_band
