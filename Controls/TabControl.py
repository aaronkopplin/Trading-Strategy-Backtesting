from PyQt5 import QtGui, QtWidgets, QtCore
import StyleInfo


class TabControl(QtWidgets.QTabWidget):
    def __init__(self):
        super(TabControl, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet(f"""
                            QTabWidget::pane {{ /* The tab widget frame */
                                border-top: 0px;
                            }}
                            QTabBar {{
                                color: white;
                                font: bold {StyleInfo.font_size}px;
                                padding: 10px;
                            }}

                            QTabBar::tab {{
                                background-color: {StyleInfo.rgb_background};
                            }}

                            QTabBar::tab:selected {{
                                background-color: {StyleInfo.rgb_button_green};
                            }}
                            """)
