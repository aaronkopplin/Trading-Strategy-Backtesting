import PyQt5.QtWidgets
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from Graph import Graph
from InfoPanel import InfoPanel
from Strategy import Account
from Controls.Panel import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import StyleInfo


class Window(QMainWindow):
    def __init__(self, candles: list):
        super().__init__()
        self.title = "Trading Bot"
        self.top = 150
        self.left = 150
        self.setMinimumWidth(1000)
        self.setMinimumHeight(500)

        self.panel = Panel(LayoutDirection.HORIZONTAL)
        self.setContentsMargins(0, 0, 0, 0)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setStyleSheet(StyleInfo.splitter_style)
        self.panel.addWidget(self.splitter)

        # graph
        self.graph = Graph(candles)
        self.graph.setSizePolicy(PyQt5.QtWidgets.QSizePolicy(PyQt5.QtWidgets.QSizePolicy.Expanding,
                                                             PyQt5.QtWidgets.QSizePolicy.Expanding))
        self.splitter.addWidget(self.graph)

        # info panel
        self.info_panel = InfoPanel(candles)
        self.info_panel.run_strategy_event = self.run_strategy_event
        self.splitter.addWidget(self.info_panel)

        self.setCentralWidget(self.panel)
        self.InitWindow()
        self.showMaximized()

    def run_strategy_event(self, account: Account):
        self.graph.strategy_run_event(account)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.info_panel.setMaximumWidth(int(self.width() / 3))

    def InitWindow(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()





