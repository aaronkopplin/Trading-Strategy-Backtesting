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

    def remove_all_rows(self):
        self.model.removeRows(0, self.rows)
        self.rows = 0

    def width_all_columns(self) -> int:
        width = 0
        for i in range(self.model.columnCount()):
            width += self.columnWidth(i)
        return width

