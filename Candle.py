class Candle:
    def __init__(self, vals: list):
        self.date_time = vals[0]
        self.open = float(vals[1])
        self.high = float(vals[2])
        self.low = float(vals[3])
        self.close = float(vals[4])
        self.adj_close = float(vals[5])
        self.volume = float(vals[6])
        self.percent = ((self.close - self.open) / self.open) * 100
        self.sma = 0
        self.upper_band = 0
        self.lower_band = 0