from PyQt5 import QtWidgets


class VerticalLayout(QtWidgets.QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)