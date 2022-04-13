from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from Candle import Candle
from Strategy import Strategy
from Strategies import *
import StyleInfo
from Controls.Graph import Graph
from Controls.Panel import *
from Controls.Button import Button
from PyQt5.QtCore import Qt
from Controls.Label import Label
from Controls.TabControl import TabControl
from ParameterPanel import ParameterPanel
import Graph as PriceGraph
from Controls.StrategyButton import StrategyButton
from Trade import Trade


class InfoPanel(Panel):
    def __init__(self, candles: list[Candle], graph: PriceGraph, strategy_run_event: Callable):
        super().__init__()
        self.graph = graph
        self.run_strategy_event = strategy_run_event
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

        self.add_strategy_buttons()

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

    def add_strategy_buttons(self):
        for strategy in strategies:
            parameters = {
                "candles": self.candles
            }
            b = StrategyButton(strategy, parameters, self.after_strategy_callback)
            self.panel.add_widget(b)

    def after_strategy_callback(self, account: Account):
        self.run_strategy_event(account)
        logs: list[(str, int)] = []
        trade: Trade
        for trade in account.trades:
            logs.append("profit: " + '${:,.2f}'.format(trade.profit)
                        + "\tamount of trade: " + '${:,.2f}'.format(trade.usd_amount)
                        + "\tacct bal after trade: " + '${:,.2f}'.format(trade.account_usd_bal))
        log_str = "\n".join([log for log in logs])
        ending_account_val = account.account_value(self.candles[len(self.candles) - 1].close)
        self.output.setPlainText(log_str)
        self.performance_graph.set_data(account.account_values)
        self.compute_statistics(account)

    def format_val(self, val: float):
        return '${:,.2f}'.format(val)

    def compute_statistics(self, account: Account):
        stats: list[str] = []
        end_bal = float(account.account_values[-1])
        begin_bal = float(account.beginning_balance)
        percent_change = "{:.00%}".format(((end_bal - begin_bal) / begin_bal))
        lowest_acct_bal = min(account.account_values)
        lowest_cash_reserves = min(account.cash_reserve_values)
        largest_profit = max(account.profits)

        stats.append(f"beginning bal: {self.format_val(begin_bal)}, ending bal: {self.format_val(end_bal)}")
        stats.append(f"percent change: {percent_change}")
        stats.append(f"lowest account value: {self.format_val(lowest_acct_bal)}")
        stats.append(f"lowest cash reserves: {self.format_val(lowest_cash_reserves)}")
        stats.append(f"largest profit: {self.format_val(largest_profit)}")

        self.statistics.setPlainText("\n".join(stat for stat in stats))



