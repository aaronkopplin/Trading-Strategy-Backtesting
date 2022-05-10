class Candle:
    def __init__(self, vals: list):
        self.__date_time: str = vals[0]
        self.__open = float(vals[1])
        self.__high = float(vals[2])
        self.__low = float(vals[3])
        self.__close = float(vals[4])
        self.__adj_close = float(vals[5])
        self.__volume = float(vals[6])
        self.__percent = ((self.__close - self.__open) / self.__open) * 100

    def open(self):
        return self.__open

    def high(self):
        return self.__high

    def low(self):
        return self.__low

    def close(self):
        return self.__close

    def green(self):
        return self.__open < self.__close

