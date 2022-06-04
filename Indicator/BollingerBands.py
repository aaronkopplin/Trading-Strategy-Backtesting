from statistics import stdev, mean
from DataClasses.Candle import Candle


def bollinger_bands(candles: list[Candle], length: int, standard_dev: int) -> tuple[list[float], list[float], list[float]]:
    def tp_(can: Candle):
        return (can.high() + can.low() + can.close()) / 3

    if length > len(candles):
        raise ValueError("cannot compute bollinger bands with a longer moving average than the number of datapoints")

    upper_band: list[float] = []
    middle: list[float] = []
    lower_band: list[float] = []
    candle: Candle

    for i in range(len(candles)):
        end = i
        start = end - length
        if start < 0:
            start = 0

        data = []
        if i == 0:
            data.append(tp_(candles[0]))
        else:
            for can in candles[start:end]:
                tp = tp_(can)
                data.append(tp)

        avg = mean(data)
        if len(data) == 1:
            dev = 0
        else:
            dev = stdev(data) * standard_dev

        upper_band.append(avg + dev)
        middle.append(avg)
        lower_band.append(avg - dev)
    return upper_band, middle, lower_band
