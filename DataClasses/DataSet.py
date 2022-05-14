from DataClasses.Collection import Collection
from DataClasses.RGBA import RGBA


class DataSet:
    def __init__(self, data: list[float], color: RGBA):
        if len(data) == 0:
            raise ValueError("cannot have collection of length 0")
        self.__data: list[Collection] = [Collection(data, color)]

    def clear(self):
        self.__data = []

    def add_collection(self, data: list[float], rgba: RGBA):
        if len(self.__data) > 0:
            if len(self.__data[0]) == 0:
                self.__data[0] = Collection(data, rgba)
                return
            if len(data) != len(self.__data[0]):
                raise ValueError("All collections must have the same number of points")
        self.__data.append(Collection(data, rgba))

    def collection_length(self):
        if len(self.__data) == 0:
            return 0
        return len(self.__data[0])

    def get_collection(self, index: int):
        return self.__data[index]

    def set_collection(self, collection: Collection, index: int):
        self.__data[index] = collection

    def collections(self) -> list[Collection]:
        return self.__data

    def num_collections(self):
        return len(self.__data)

    def min_value(self):
        min_ = float("inf")
        if self.collection_length() == 0:
            raise ValueError("collection is empty")
        for collection in self.collections():
            for point in collection:
                if point < min_:
                    min_ = point
        return min_

    def min_value_between_indexes(self, start: int, end: int):
        min_ = float("inf")
        if self.collection_length() < start or self.collection_length() < end:
            raise ValueError("indexes exceed collection length")
        for collection in self.collections():
            for i in range(start, end):
                point = collection[i]
                if point < min_:
                    min_ = point
        return min_

    def max_value(self):
        max_ = float("-inf")
        if self.collection_length() == 0:
            raise ValueError("collection is empty")
        for collection in self.collections():
            for point in collection:
                if point > max_:
                    max_ = point
        return max_

    def max_value_between_indexes(self, start: int, end: int):
        max_ = float("-inf")
        if self.collection_length() < start or self.collection_length() < end:
            raise ValueError("indexes exceed collection length")
        for collection in self.collections():
            for i in range(start, end):
                point = collection[i]
                if point > max_:
                    max_ = point
        return max_
