from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyleOption, QStyle

from Controls.LayoutDirection import LayoutDirection
import StyleInfo
from Controls.VerticalLayout import VerticalLayout


class Panel(QtWidgets.QWidget):
    def __init__(self):
        super(Panel, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(VerticalLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(f"""
                            QWidget {{
                                background-color: {StyleInfo.rgb_panel};
                                color: white;
                                font: {StyleInfo.font_size}px;
                            }}
                            """)

    def set_layout(self, direction: LayoutDirection):
        # re-parent the layout
        # explanation: https://stackoverflow.com/questions/10416582/replacing-layout-on-a-qwidget-with-another-layout
        new_wid = QtWidgets.QWidget()
        new_wid.setLayout(self.layout())

        layout = None
        if direction == LayoutDirection.VERTICAL:
            layout = QtWidgets.QVBoxLayout()
        elif direction == LayoutDirection.HORIZONTAL:
            layout = QtWidgets.QHBoxLayout()
        elif direction == LayoutDirection.GRID:
            layout = QtWidgets.QGridLayout()

        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def add_widget(self, w: QtWidgets.QWidget):
        self.layout().addWidget(w)

    def add_item(self, item: QtWidgets.QSpacerItem):
        self.layout().addItem(item)

    # I HAVE NO IDEA WHY THIS IS NEEDED
    # sourced from: https://stackoverflow.com/questions/18344135/why-do-stylesheets-not-work-when-subclassing-qwidget-and-using-q-object/32889486#32889486
    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)