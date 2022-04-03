from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Candle import Candle
from Strategy import Account, strategy_1, Trade
import StyleInfo


class InfoPanel(QtWidgets.QWidget):
    def __init__(self, candles: list[Candle]):
        super().__init__()
        self.run_strategy_event = None
        self.candles: list[Candle] = candles
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet(f"""
                            background-color: {StyleInfo.panel_color};
                            color: white;
                            font-size: {StyleInfo.font_size}pt;
                            border: none;
                            
                            """)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.panel = QWidget()
        self.layout.addWidget(self.panel)
        self.panel_layout = QVBoxLayout()
        self.panel_layout.setContentsMargins(0, 0, 0, 0)
        self.panel.setLayout(self.panel_layout)

        # main label
        main_label = QtWidgets.QLabel("STRATEGIES")
        main_label.setStyleSheet(f"font: bold {StyleInfo.button_font_size}px;")
        main_label.setContentsMargins(0, 0, 0, 0)
        main_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        main_label.setAlignment(Qt.AlignCenter)
        self.panel_layout.addWidget(main_label)

        # second label
        self.strategy_1_button = QPushButton("STRATEGY 1")
        self.strategy_1_button.setStyleSheet(StyleInfo.button_style)
        self.strategy_1_button.clicked.connect(self.run_strategy_1)
        self.panel_layout.addWidget(self.strategy_1_button)

        # bottom spacer to push everything to top
        spacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.panel_layout.addItem(spacer)

        self.output = QPlainTextEdit()
        self.output.setStyleSheet(f"""
                                   background-color: {StyleInfo.background_color_rgb};
                                   """)
        self.output.setMinimumHeight(int(self.panel.height() / 2))

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
                                 QTabBar::tab {{
                                     background-color: {StyleInfo.background_color_rgb}; 
                                     font: bold {16}px;
                                 }} 
                                    
                                 QTabBar::tab:selected {{ 
                                     background-color: {StyleInfo.button_green_color_rgb}; 
                                     font: bold {16}px;
                                 }}
                                 """)
        self.tabs.setContentsMargins(0, 0, 0, 0)
        self.tabs.addTab(self.output, "OUTPUT")
        self.panel_layout.addWidget(self.tabs)

        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "CHART")
        self.tab2.setStyleSheet(f"background-color: {StyleInfo.background_color_rgb};")

    def run_strategy_1(self):
        account: Account = strategy_1(self.candles)
        self.run_strategy_event(account)
        logs: list[(str, int)] = []
        trade: Trade
        for trade in account.trades:
            buy_price = '${:,.2f}'.format(trade.buy_price)
            logs.append((f"bought {trade.crypto_amount} at {buy_price}", trade.buy_candle_index))
            if trade.sell_candle_index:
                sell_price = "${:,.2f}".format(trade.sell_price)
                logs.append((f"sold {trade.crypto_amount} at {sell_price}", trade.sell_candle_index))

        logs = sorted(logs, key=lambda log: log[1])  # sort based on candle index
        log_str = "\n".join([log[0] for log in logs])
        ending_account_val = account.account_value(self.candles[len(self.candles) - 1].close)
        self.output.setPlainText(log_str)

