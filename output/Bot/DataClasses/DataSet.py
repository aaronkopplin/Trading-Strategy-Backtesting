from DataClasses.Collection import Collection
from DataClasses.RGBA import RGBA
import typing


class DataSet:
    def __init__(self, title: str, data: list[float], color: RGBA):
        self.__data: typing.Dict[str, Collection] = {title: Collection(title, data, color)}
        self.global_min = None
        self.global_max = None
        self.local_mins = {}
        self.local_maxes = {}

    def __reset_global_values(self):
        self.global_min = None
        self.global_max = None
        self.local_mins = {}
        self.local_maxes = {}

    def clear(self):
        self.__data = []

    def add_collection(self, title: str, data: list[float], rgba: RGBA):
        self.__data[title] = Collection(title, data, rgba)
        self.__reset_global_values()

    def contains(self, title: str):
        return title in self.__data

    def collection_length(self):
        if len(self.__data) == 0:
            return 0
        return len(list(self.__data.values())[0])

    def collections(self) -> list[Collection]:
        return list(self.__data.values())

    def num_collections(self):
        return len(self.__data)

    def min_value(self):
        if self.global_min:
            return self.global_min

        min_ = float("inf")
        if len(self.collections()) == 0 or len(self.collections()[0]) == 0:
            return min_

        if self.collection_length() == 0:
            raise ValueError("collection is empty")
        for collection in self.collections():
            m = min(collection)
            if m < min_:
                min_ = m

        self.global_min = min_
        return min_

    def min_value_between_indexes(self, start: int, end: int):
        min_ = float("inf")
        if len(self.collections()) == 0 or len(self.collections()[0]) == 0:
            return min_

        if self.collection_length() < start or self.collection_length() < end:
            raise ValueError("indexes exceed collection length")

        if self.local_mins.get((start, end)):
            return self.local_mins[(start, end)]

        for collection in self.collections():
            m = min(collection[start:end])
            if m < min_:
                min_ = m

        self.local_mins[(start, end)] = min_
        return min_

    def max_value(self):
        max_ = float("-inf")
        if len(self.collections()) == 0 or len(self.collections()[0]) == 0:
            return max_

        if self.collection_length() == 0:
            raise ValueError("collection is empty")
        for collection in self.collections():
            m = max(collection)
            if m > max_:
                max_ = m

        self.global_max = max_
        return max_

    def max_value_between_indexes(self, start: int, end: int):
        max_ = float("-inf")
        if self.collection_length() < start or self.collection_length() < end:
            raise ValueError("indexes exceed collection length")

        if len(self.collections()) == 0 or len(self.collections()[0]) == 0:
            return max_

        if self.local_maxes.get((start, end)):
            return self.local_maxes[(start, end)]

        for collection in self.collections():
            m = max(collection[start:end])
            if m > max_:
                max_ = m

        self.local_maxes[(start, end)] = max_
        return max_
