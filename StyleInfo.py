from PyQt5.QtGui import QPainter, QColor, QFont

rgb_panel: str = "rgb(18, 28, 38)"
rgb_background: str = "rgb(6, 15, 20)"
rgb_button_green = "rgb(62, 180, 68)"
rgb_grid_line = "rgb(60, 67, 70)"
rgb_splitter: str = "rgb(60, 67, 70)"

color_green_candle = QColor(103, 191, 82)
color_red_candle = QColor(244, 103, 54)
color_background = QColor(6, 15, 20)
color_grid_line = QColor(60, 67, 70)
color_cursor = QColor(108, 112, 117)
color_bollinger_band = QColor(102, 178, 255)
color_strategy_buy = QColor(204, 255, 179, 50)
color_strategy_sell = QColor(255, 179, 179, 50)

pen_width = 1
num_candles_per_grid_line = 5
num_horizontal_gridlines = 20
font_size = 16


splitter_style = f"background-color: {rgb_grid_line}"
