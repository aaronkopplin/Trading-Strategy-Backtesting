from PyQt5.QtWidgets import *
from DataClasses.Candle import Candle
from Controls.Panel import *
from Controls.Button import Button
from PyQt5.QtCore import Qt
from Controls.Label import Label
from Controls.TabControl import TabControl
from DataClasses.Trade import Trade
from typing import Callable
from Controls.LineChart import LineChart
from DataClasses.Account import Account
from Controls.Splitter import Splitter
from DataClasses.RGBA import RGBA
import StyleInfo
from Controls.StatisticsTable import StatisticsTable
from Controls.OutputChart import OutputChart


class InfoPanel(Panel):
    def __init__(self):
        super().__init__()
        self.splitter = Splitter(LayoutDirection.VERTICAL)
        self.add_widget(self.splitter)

        self.statistics = StatisticsTable()
        self.statistics.setStyleSheet(f"""QHeaderView::section {{
                                                background-color: {StyleInfo.rgb_splitter};
                                                color: white;
                                                padding-left: 4px;
                                                border: 1px solid #6c6c6c;
                                            }}
                                      """)
        self.statistics.verticalHeader().setVisible(False)

        self.stat_panel = Panel()
        self.stat_panel.add_widget(self.statistics)
        self.splitter.addWidget(self.stat_panel)

        self.output = OutputChart("PERFORMANCE", [0], RGBA(255, 255, 255, 255))
        self.add_output()

    def add_output(self):
        self.output.set_draw_y_axis(True)
        self.splitter.addWidget(self.output)
        self.stat_panel.resize(self.width(), int(self.height() / 2))
        self.output.resize(self.width(), int(self.height() / 2))

    def add_collection(self, title: str, data: list[float], rgba: RGBA):
        self.output.add_collection(title, data, rgba)
        self.output.zoom_out_max()

    def clear_performance(self):
        self.output.clear_datasets()
        self.statistics.remove_all_rows()