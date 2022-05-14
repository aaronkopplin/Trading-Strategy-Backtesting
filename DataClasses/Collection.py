from DataClasses.RGBA import RGBA


class Collection(list):
    def __init__(self, title: str, data: list, color: RGBA):
        super(Collection, self).__init__(data)
        self.color = color
        self.title = title
