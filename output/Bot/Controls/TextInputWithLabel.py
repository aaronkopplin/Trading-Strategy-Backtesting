from Controls.Panel import *
from Controls.Label import Label


class TextInputWithLabel(Panel):
    def __init__(self, text: str):
        super().__init__()
        self.text_input = QtWidgets.QLineEdit()
        self.label = Label()
        self.label.setText(text)

        self.set_layout(LayoutDirection.HORIZONTAL)
        self.add_widget(self.label)
        self.add_widget(self.text_input)

    def get_text(self) -> str:
        return self.text_input.text()

    def set_text(self, text: str):
        self.text_input.setText(text)
