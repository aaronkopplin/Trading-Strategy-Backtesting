from PyQt5 import QtGui, QtWidgets, QtCore
import StyleInfo
from Controls.LayoutDirection import LayoutDirection


class Splitter(QtWidgets.QSplitter):
    def __init__(self, direction: LayoutDirection):
        if direction == LayoutDirection.VERTICAL:
            super(Splitter, self).__init__(QtCore.Qt.Vertical)
        if direction == LayoutDirection.HORIZONTAL:
            super(Splitter, self).__init__(QtCore.Qt.Horizontal)

        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(f"""
                            QSplitter::handle:vertical {{
                                background-color: {StyleInfo.rgb_splitter};
                            }}
                            
                            QSplitter::handle:horizontal {{
                                background-color: {StyleInfo.rgb_splitter};
                            }}
                            
                            color: white;
                            background-color: {StyleInfo.rgb_panel};
                            """)
