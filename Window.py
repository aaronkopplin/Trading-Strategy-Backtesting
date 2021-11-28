import PyQt5.QtWidgets
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from Graph import Graph
from InfoPanel import InfoPanel
from Strategy import Account


class Window(QMainWindow):
    def __init__(self, candles: list):
        super().__init__()
        self.title = "Trading Bot"
        self.top = 150
        self.left = 150
        self.setMinimumWidth(1000)
        self.setMinimumHeight(500)
        self.panel = QtWidgets.QWidget()
        self.setContentsMargins(0, 0, 0, 0)
        self.panel.setContentsMargins(0, 0, 0, 0)
        self.panel_layout = QtWidgets.QGridLayout()
        self.panel_layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: white; ")

        # graph
        self.graph = Graph(candles)
        self.graph.setSizePolicy(PyQt5.QtWidgets.QSizePolicy(PyQt5.QtWidgets.QSizePolicy.Expanding,
                                                             PyQt5.QtWidgets.QSizePolicy.Expanding))
        self.panel_layout.addWidget(self.graph, 0, 0)

        # info panel
        self.info_panel = InfoPanel(candles)
        self.info_panel.run_strategy_event = self.run_strategy_event
        self.panel_layout.addWidget(self.info_panel, 0, 1)

        self.panel.setLayout(self.panel_layout)
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





