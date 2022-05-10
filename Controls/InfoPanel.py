from PyQt5.QtWidgets import *
from DataClasses.Candle import Candle
from Controls.Panel import *
from Controls.Button import Button
from PyQt5.QtCore import Qt
from Controls.Label import Label
from Controls.TabControl import TabControl
from Controls.StrategyButton import StrategyButton
from DataClasses.Trade import Trade
from typing import Callable
from Controls.LineChart import LineChart
from DataClasses.Account import Account


class InfoPanel(Panel):
    def __init__(self, candles: list[Candle], graph: LineChart, strategy_run_event: Callable):
        super().__init__()
        self.graph = graph
        self.run_strategy_event = strategy_run_event
        self.candles: list[Candle] = candles
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # create a panel to override the splitter color
        self.panel = Panel()
        self.add_widget(self.panel)

        # bottom spacer to push everything to top
        # self.spacer = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.panel.add_item(self.spacer)

        self.tabs = None
        self.statistics = None
        self.output = None
        self.add_tabs()

    def add_tabs(self):
        self.tabs = TabControl()
        self.tabs.setContentsMargins(0, 0, 0, 0)
        self.add_output()
        self.add_widget(self.tabs)
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

    def after_strategy_callback(self, account: Account):
        self.run_strategy_event(account)
        logs: list[(str, int)] = []
        trade: Trade
        for trade in account.trades:
            logs.append("profit: " + '${:,.2f}'.format(trade.profit)
                        + "\tamount of trade: " + '${:,.2f}'.format(trade.usd_amount)
                        + "\tacct bal after trade: " + '${:,.2f}'.format(trade.account_usd_bal))
        log_str = "\n".join([log for log in logs])
        ending_account_val = account.account_value(self.candles[len(self.candles) - 1].__close)
        self.output.setPlainText(log_str)
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
        fees_paid = account.fees_taken

        stats.append(f"beginning bal: {self.format_val(begin_bal)}, ending bal: {self.format_val(end_bal)}")
        stats.append(f"percent change: {percent_change}")
        stats.append(f"lowest account value: {self.format_val(lowest_acct_bal)}")
        stats.append(f"lowest cash reserves: {self.format_val(lowest_cash_reserves)}")
        stats.append(f"largest profit: {self.format_val(largest_profit)}")
        stats.append(f"fees paid: {self.format_val(fees_paid)}")

        self.statistics.setPlainText("\n".join(stat for stat in stats))



