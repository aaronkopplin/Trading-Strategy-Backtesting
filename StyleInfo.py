from PyQt5.QtGui import QPainter, QColor, QFont


panel_color = "rgb(18, 28, 38)"
pen_width = 1
background_color = QColor(6, 15, 20)
background_color_rgb = "rgb(6, 15, 20)"
button_green_color_rgb = "rgb(62, 180, 68)"
green_candle = QColor(103, 191, 82)
red_candle = QColor(244, 103, 54)
gridline_color = QColor(60, 67, 70)
gridline_color_rgb = "rgb(60, 67, 70)"
num_candles_per_gridline = 5
num_horizontal_gridlines = 20
cursor_color = QColor(108, 112, 117)
bollinger_band_color = QColor(102, 178, 255)
font_size = 12
strategy_buy_candle = QColor(204, 255, 179, 25)
strategy_sell_candle = QColor(255, 179, 179, 25)

button_style = f"background-color: {button_green_color_rgb};" \
               f"border-style: none;" \
               f"font: bold {16}px;" \
               f"padding: 10px;" \
               f"margin: 2px;"

splitter_style = f"background-color: {gridline_color_rgb}"
