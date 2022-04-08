from PullData import read_candles
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from Window import Window


def open_application(candles: list):
    App = QApplication(sys.argv)
    window = Window(candles)
    sys.exit(App.exec())


candles = read_candles()
print("percent gain for timeframe", ((candles[len(candles) - 1].open - candles[0].open ) / candles[0].open) * 100)

open_application(candles)

