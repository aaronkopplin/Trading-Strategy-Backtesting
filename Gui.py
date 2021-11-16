from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QBrush, QPen, QPainterPath
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from Candle import Candle
from Window import Window


def open_application(candles: list):
    App = QApplication(sys.argv)
    window = Window(candles)
    sys.exit(App.exec())
