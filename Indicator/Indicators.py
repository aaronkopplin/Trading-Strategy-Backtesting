from DataClasses.Candle import Candle
from Indicator.BollingerBands import bollinger_bands
from Indicator.MovingAverages import moving_average


class Indicators:
    def __init__(self, candles: list[Candle]):
        self.__candles = candles
        self.__bands = {}
        self.__smas = {}

    def bollinger_bands(self, index: int, length: int, standard_dev: int):
        key = (length, standard_dev)
        if self.__bands.get(key):
            l, m, u = self.__bands[key]
            return l[index], m[index], u[index]

        upper, middle, lower = bollinger_bands(self.__candles, length, standard_dev)
        self.__bands[key] = upper, middle, lower

        return upper[index], middle[index], lower[index]

    def sma_closes(self,index: int, period: int):
        key = "closes"
        if self.__smas.get(key):
            return self.__smas[key][index]

        data = [can.close() for can in self.__candles]
        sma = moving_average(data, period)
        self.__smas[key] = sma
        return sma[index]
