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
from ParameterPanel import ParameterPanel
import Graph as PriceGraph


class InfoPanel(Panel):
    def __init__(self, candles: list[Candle], graph: PriceGraph):
        super().__init__()
        self.graph = graph
        self.run_strategy_event = None
        self.candles: list[Candle] = candles
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # create a panel to override the splitter color
        self.panel = Panel()
        self.add_widget(self.panel)

        # main label
        main_label = Label()
        main_label.setText("STRATEGIES")
        main_label.setAlignment(Qt.AlignCenter)
        self.panel.add_widget(main_label)

        self.add_parameters()

        # bottom spacer to push everything to top
        self.spacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.panel.add_item(self.spacer)

        # second label
        self.strategy_1_button = Button()
        self.strategy_1_button.setText("STRATEGY 1")
        self.strategy_1_button.clicked.connect(self.run_strategy_1)
        self.panel.add_widget(self.strategy_1_button)

        self.clear_button = Button()
        self.clear_button.setText("CLEAR")
        self.clear_button.clicked.connect(self.clear_graph)
        self.panel.add_widget(self.clear_button)

        self.add_tabs()

    def clear_graph(self):
        self.graph.clear_chart()
        self.output.setPlainText("")
        self.performance_graph.clear_graph()
        self.statistics.setPlainText("")

    def add_parameters(self):
        self.parameters = ParameterPanel()
        self.panel.add_widget(self.parameters)

    def add_tabs(self):
        self.tabs = TabControl()
        self.tabs.setContentsMargins(0, 0, 0, 0)
        self.add_output()
        self.add_widget(self.tabs)
        self.add_performance()
        self.add_statistics()

    def add_statistics(self):
        self.statistics = QPlainTextEdit()
        self.statistics.setStyleSheet(f"""
                                           background-color: {StyleInfo.rgb_background}; 
                                           color: white;
                                           font: {StyleInfo.font_size}px;
                                           """)
        self.tabs.addTab(self.statistics, "STATISTICS")

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
        account: Account = strategy_1(candles=self.candles, parameters=self.parameters.get_parameters())
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
        self.compute_statistics(account)

    def compute_statistics(self, account: Account):
        stats: list[str] = []
        end_bal = float(account.account_values[-1])
        begin_bal = float(account.beginning_balance)
        percent_change = "{:.0%}".format(((end_bal - begin_bal) / begin_bal))

        stats.append(f"beginning bal: {begin_bal}, ending bal: {end_bal}")
        stats.append(f"percent change: {percent_change}")

        self.statistics.setPlainText("\n".join(stat for stat in stats))



