from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from Candle import Candle
from Strategy import Account, strategy_1, Trade
import StyleInfo
from Controls.Graph import Graph
from Controls.Panel import *
from Controls.Button import Button
from PyQt5.QtCore import Qt
from Controls.Label import Label
from Controls.TabControl import TabControl


class InfoPanel(Panel):
    def __init__(self, candles: list[Candle]):
        super().__init__()
        self.run_strategy_event = None
        self.candles: list[Candle] = candles
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # create a panel to override the splitter color
        self.panel = Panel()
        self.add_widget(self.panel)

        # main label
        main_label = Label()
        main_label.setText("STRATEGIES")
        main_label.setContentsMargins(0, 0, 0, 0)
        main_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        main_label.setAlignment(Qt.AlignCenter)
        self.panel.add_widget(main_label)

        # second label
        self.strategy_1_button = Button()
        self.strategy_1_button.setText("STRATEGY 1")
        self.strategy_1_button.clicked.connect(self.run_strategy_1)
        self.panel.add_widget(self.strategy_1_button)

        # bottom spacer to push everything to top
        self.spacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.panel.add_item(self.spacer)

        self.tabs = TabControl()
        self.tabs.setContentsMargins(0, 0, 0, 0)
        self.add_output()

        self.add_widget(self.tabs)
        self.add_performance()

    def add_output(self):
        self.output = QPlainTextEdit()
        self.output.setMinimumHeight(int(self.height() / 2))
        self.output.setStyleSheet(f"""
                                   background-color: {StyleInfo.rgb_background}; 
                                   color: white;
                                   font: {StyleInfo.font_size}px;
                                   """)
        self.tabs.addTab(self.output, "OUTPUT")

    def add_performance(self):
        self.performance_graph = Graph()
        self.tabs.addTab(self.performance_graph, "PERFORMANCE")

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
        self.performance_graph.set_data(account.account_values)

