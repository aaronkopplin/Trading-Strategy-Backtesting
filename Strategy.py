from typing import Callable
from Account import Account
from Trade import Trade


class Strategy:
    def __init__(self, name: str, strategy: Callable):
        self.strategy = strategy
        self.name = name


