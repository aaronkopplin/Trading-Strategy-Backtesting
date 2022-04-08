from PyQt5 import QtGui, QtWidgets, QtCore
import StyleInfo


class Label(QtWidgets.QLabel):
    def __init__(self):
        super(Label, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(f"""font: bold {StyleInfo.font_size}px;
                                color: white;""")
