from Controls.LineChart import LineChart
from DataClasses.Candle import Candle
from DataClasses.RGBA import RGBA
from overrides import overrides
from Utilities.TextUtilities import format_as_two_decimal_price


class OutputChart(LineChart):
    def __init__(self, title: str, data: list[float], rgba: RGBA):
        super().__init__(title, data, rgba)

    @overrides
    def format_text_for_y_axis(self, text: float) -> str:
        return format_as_two_decimal_price(text)