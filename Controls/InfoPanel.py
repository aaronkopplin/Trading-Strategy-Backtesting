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
from Controls.Splitter import Splitter
from DataClasses.RGBA import RGBA


class InfoPanel(Panel):
    def __init__(self, candles: list[Candle], graph: LineChart, strategy_run_event: Callable):
        super().__init__()
        self.splitter = Splitter(LayoutDirection.VERTICAL)
        self.add_widget(self.splitter)

        self.statistics = QPlainTextEdit()
        self.statistics.setStyleSheet(f"border: none;")
        self.stat_panel = Panel()
        self.stat_panel.add_widget(self.statistics)
        self.splitter.addWidget(self.stat_panel)

        self.output = LineChart([i for i in range(100)], RGBA(255, 255, 255, 255))
        self.splitter.addWidget(self.output)

        self.stat_panel.resize(self.width(), int(self.height() / 2))
        self.output.resize(self.width(), int(self.height() / 2))




    # def after_strategy_callback(self, account: Account):
    #     self.run_strategy_event(account)
    #     logs: list[(str, int)] = []
    #     trade: Trade
    #     for trade in account.trades:
    #         logs.append("profit: " + '${:,.2f}'.format(trade.profit)
    #                     + "\tamount of trade: " + '${:,.2f}'.format(trade.usd_amount)
    #                     + "\tacct bal after trade: " + '${:,.2f}'.format(trade.account_usd_bal))
    #     log_str = "\n".join([log for log in logs])
    #     ending_account_val = account.account_value(self.candles[len(self.candles) - 1].__close)
    #     self.output.setPlainText(log_str)
    #     self.compute_statistics(account)
    #
    # def format_val(self, val: float):
    #     return '${:,.2f}'.format(val)
    #
    # def compute_statistics(self, account: Account):
    #     stats: list[str] = []
    #     end_bal = float(account.account_values[-1])
    #     begin_bal = float(account.beginning_balance)
    #     percent_change = "{:.00%}".format(((end_bal - begin_bal) / begin_bal))
    #     lowest_acct_bal = min(account.account_values)
    #     lowest_cash_reserves = min(account.cash_reserve_values)
    #     largest_profit = max(account.profits)
    #     fees_paid = account.fees_taken
    #
    #     stats.append(f"beginning bal: {self.format_val(begin_bal)}, ending bal: {self.format_val(end_bal)}")
    #     stats.append(f"percent change: {percent_change}")
    #     stats.append(f"lowest account value: {self.format_val(lowest_acct_bal)}")
    #     stats.append(f"lowest cash reserves: {self.format_val(lowest_cash_reserves)}")
    #     stats.append(f"largest profit: {self.format_val(largest_profit)}")
    #     stats.append(f"fees paid: {self.format_val(fees_paid)}")
    #
    #     self.statistics.setPlainText("\n".join(stat for stat in stats))
    #
    #
    #
