from Controls.Button import Button
from DataClasses.Strategy import Strategy
from typing import Callable


class StrategyButton(Button):
    def __init__(self, strategy: Strategy, parameters: dict, callback: Callable):
        super().__init__()
        self.strategy = strategy
        self.setText(self.strategy.name)
        self.clicked.connect(lambda: self.strategy.strategy(parameters, callback))
        self.parameters = parameters
