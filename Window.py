import PyQt5.QtWidgets
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from Graph import Graph


class Window(QMainWindow):
    def __init__(self, candles: list):
        super().__init__()
        self.title = "Trading Bot"
        self.top = 150
        self.left = 150
        self.panel = QtWidgets.QWidget()
        self.setContentsMargins(0, 0, 0, 0)
        self.panel.setContentsMargins(0, 0, 0, 0)
        self.panel_layout = QtWidgets.QGridLayout()
        self.panel_layout.setContentsMargins(0, 0, 0, 0)

        # graph
        self.graph = Graph(candles)
        self.graph.setSizePolicy(PyQt5.QtWidgets.QSizePolicy(PyQt5.QtWidgets.QSizePolicy.Expanding,
                                                             PyQt5.QtWidgets.QSizePolicy.Expanding))
        self.panel_layout.addWidget(self.graph, 0, 0)

        # info panel
        self.info_panel = QtWidgets.QWidget()
        self.info_panel.setFixedSize(50, 50)
        self.info_panel.setStyleSheet("background-color: yellow")
        self.panel_layout.addWidget(self.info_panel, 0, 1)

        self.panel.setLayout(self.panel_layout)
        self.setCentralWidget(self.panel)
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()





