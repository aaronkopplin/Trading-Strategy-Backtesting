from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *


class StatisticsTable(QTableView):
    def __init__(self):
        super().__init__()
        self.rows = 0
        self.model = QStandardItemModel()
        self.setModel(self.model)

    def set_column_headers(self, *args):
        self.model.setHorizontalHeaderLabels(args)

    def add_row(self, *args):
        for i in range(len(args)):
            self.model.setItem(self.rows, i, QStandardItem(str(args[i])))
        self.rows += 1
        self.resizeColumnsToContents()

