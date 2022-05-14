from Controls.InfoPanel import InfoPanel
from PyQt5.QtWidgets import *
from Controls.Splitter import Splitter
from Controls.LayoutDirection import LayoutDirection
from Strategy1 import Strategy1
import StyleInfo
from Controls.ChartAndIndicator import ChartAndIndicator
from Controls.VerticalLayout import VerticalLayout


class Window(QMainWindow):
    def __init__(self, candles: list):
        super().__init__()
        self.title = "Trading Bot"
        self.top = 150
        self.left = 150
        self.setMinimumWidth(1000)
        self.setMinimumHeight(500)
        self.setContentsMargins(0, 0, 0, 0)
        self.candles = candles

        # file menu
        strategy_action = QAction("&Strategy 1", self)
        strategy_action.setShortcut("Ctrl+R")
        strategy_action.triggered.connect(self.run_strategy_event)

        main_menu: QMenuBar = self.menuBar()
        main_menu.setStyleSheet(f"""background-color: {StyleInfo.rgb_panel}; 
                                    color: white; 
                                    font: {StyleInfo.font_size}px;
                                 """)
        file_menu: QMenu = main_menu.addMenu("&FILE")
        file_menu.addAction(strategy_action)

        # indicators menu
        bollinger_bands_action = QAction("Bollinger Bands", self)
        bollinger_bands_action.setShortcut("Ctrl+B")
        bollinger_bands_action.triggered.connect(self.bollinger_bands_event)

        indicators_menu = main_menu.addMenu("&INDICATORS")
        indicators_menu.addAction(bollinger_bands_action)

        # splitter
        self.splitter = Splitter(LayoutDirection.HORIZONTAL)

        # graph
        self.chart: ChartAndIndicator = ChartAndIndicator(self.candles)
        self.chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.splitter.addWidget(self.chart)

        # info panel
        self.info_panel = InfoPanel(candles, self.chart.candle_chart(), self.run_strategy_event)
        # self.info_panel = InfoPanel()
        self.info_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.splitter.addWidget(self.info_panel)

        self.splitter.widget(0).resize(int(self.width() / 2), self.height())
        self.splitter.widget(1).resize(int(self.width() / 2), self.height())

        # finish initialization
        self.setCentralWidget(self.splitter)
        self.InitWindow()
        self.showMaximized()

    def bollinger_bands_event(self):
        self.chart.indicator_checked("Bollinger Bands", True)

    def run_strategy_event(self):
        self.chart.clear_strategy()

        # TODO, instead of passing in the chart, create the strategy, then collect the strategy data, then plot on the chart
        self.strategy = Strategy1(self.chart, self.candles)

    # def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
    #     self.info_panel.setMaximumWidth(int(self.width() / 3))

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.show()





