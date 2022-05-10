# from __future__ import annotations
#
#
# class Node:
#     def __init__(self, data: float):
#         self.__prev: Node = None
#         self.__data = data
#         self.__next: Node = None
#
#     def data(self):
#         return self.__data
#
#     def set_prev(self, node: Node):
#         self.__prev = node
#
#     def prev(self):
#         return self.__prev
#
#     def set_next(self, node: Node):
#         self.__next = node
#
#     def next(self):
#         return self.__next
#
#     def index(self):
#         current = self
#         count = 0
#         while current.prev() is not None:
#             current = current.prev()
#             count += 1
#         return count
#
