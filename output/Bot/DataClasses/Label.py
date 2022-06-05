from DataClasses.RGBA import RGBA


class Label:
    def __init__(self, y_value: float, x_index: int, text: str, color: RGBA):
        self.y_value = y_value
        self.x_index = x_index
        self.text = text
        self.color = color