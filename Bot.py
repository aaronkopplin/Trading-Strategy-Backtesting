from Utilities.PullData import read_candles
from PyQt5.QtWidgets import QApplication
import sys
from Controls.Window import Window

# candles = read_candles()
App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())


