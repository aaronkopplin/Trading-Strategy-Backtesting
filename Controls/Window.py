from Controls.InfoPanel import InfoPanel
from PyQt5.QtWidgets import *
from Controls.Splitter import Splitter
from Controls.LayoutDirection import LayoutDirection
from Strategy1 import Strategy1
from DataClasses.Strategy import Strategy
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
        self.strategy: Strategy = None

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

        delete_action = QAction("&Delete Strategies", self)
        delete_action.setShortcut("Ctrl+D")
        delete_action.triggered.connect(self.clear_strategies_event)
        file_menu.addAction(delete_action)

        # indicators menu
        bollinger_bands_action = QAction("Bollinger Bands", self)
        bollinger_bands_action.setShortcut("Ctrl+B")
        bollinger_bands_action.triggered.connect(self.bollinger_bands_event)

        indicators_menu = main_menu.addMenu("&INDICATORS")
        indicators_menu.addAction(bollinger_bands_action)

        clear_indicators_action = QAction("Clear Indicators", self)
        clear_indicators_action.triggered.connect(self.clear_indicators_event)
        indicators_menu.addAction(clear_indicators_action)

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

    def clear_indicators_event(self):
        self.chart.clear_strategy()

    def clear_strategies_event(self):
        self.chart.clear_strategy()
        self.info_panel.clear_performance()

    def bollinger_bands_event(self):
        self.chart.indicator_checked("Bollinger Bands", True)

    def run_strategy_event(self):
        self.chart.clear_strategy()
        self.strategy = Strategy1()
        self.strategy.set_chart(self.chart)
        self.strategy.set_candles(self.candles)
        self.strategy.set_performance_chart(self.info_panel)
        self.strategy.run()


    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.show()
