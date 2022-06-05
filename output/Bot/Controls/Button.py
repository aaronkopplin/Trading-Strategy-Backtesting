from PyQt5 import QtGui, QtWidgets, QtCore
import StyleInfo


class Button(QtWidgets.QPushButton):
    def __init__(self):
        super(Button, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(f"""background-color: {StyleInfo.rgb_button_green};
                                font: bold {StyleInfo.font_size}px;
                                padding: 10px;
                                margin: 2px;
                                color: white;""")
