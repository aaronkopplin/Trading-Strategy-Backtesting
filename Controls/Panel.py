from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyleOption, QStyle
from PyQt5 import QtGui
from Controls.LayoutDirection import LayoutDirection
import StyleInfo
from Controls.VerticalLayout import VerticalLayout
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt


class Panel(QtWidgets.QWidget):
    def __init__(self):
        super(Panel, self).__init__()
        self.painter: QPainter = None
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(VerticalLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.mouse_down = False
        self.mouse_entered = False
        self.setMouseTracking(True)
        self.setStyleSheet(f"""
                            QWidget {{
                                background-color: {StyleInfo.rgb_panel};
                                color: white;
                                font: {StyleInfo.font_size}px;
                            }}
                            """)
        self.handle_mouse_events = True

    def set_handle_mouse_events(self, handle: bool):
        self.handle_mouse_events = handle

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        if self.handle_mouse_events:
            if a0.angleDelta().y() < 0:  # zoom out
                self.zoom_out()

            if a0.angleDelta().y() > 0:  # zoom in
                self.zoom_in()
            # self.compute_vertical_gridlines()
            self.update()

    def zoom_in(self):
        pass

    def zoom_out(self):
        pass

    def zoom_rate(self) -> int:
        pass

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouse_down = True
        self.update()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouse_down = False
        self.update()

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        self.mouse_entered = True
        self.update()

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.mouse_entered = False
        self.update()

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

    def draw_background(self):
        #  draw background
        self.painter.setPen(QPen(StyleInfo.color_background, StyleInfo.pen_width, Qt.SolidLine))
        self.painter.setBrush(QBrush(StyleInfo.color_background, Qt.SolidPattern))
        self.painter.drawRect(0, 0, self.width(), self.height())

    def draw_objects(self):
        # use self.painter to draw objects
        pass

    # I HAVE NO IDEA WHY THIS IS NEEDED
    # sourced from: https://stackoverflow.com/questions/18344135/why-do-stylesheets-not-work-when-subclassing-qwidget-and-using-q-object/32889486#32889486
    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

        self.painter = QPainter(self)
        self.draw_background()
        self.painter.setRenderHint(QPainter.HighQualityAntialiasing)
        self.draw_objects()
        self.painter.end()
