from Controls.Panel import *
from Controls.TextInputWithLabel import TextInputWithLabel


class ParameterPanel(Panel):
    def __init__(self):
        super().__init__()
        self.percent_per_trade_input = TextInputWithLabel("Percent of cash per trade: ")
        self.add_widget(self.percent_per_trade_input)

    def percent_per_trade(self) -> float:
        text = self.percent_per_trade_input.get_text()
        return int(text) if text.isdigit() else None

    def get_parameters(self) -> dict:
        return {
            "percent_per_trade": self.percent_per_trade()
        }