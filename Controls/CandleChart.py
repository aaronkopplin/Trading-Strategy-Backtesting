from PyQt5.QtGui import QPainter
from Controls.LineChart import LineChart
from Candle import Candle
import overrides


class CandleChart(LineChart):
    def __init__(self, data: list):
        super().__init__(data)

