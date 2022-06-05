# from DataClasses.Node import Node
#
#
# class LinkedList:
#     def __init__(self, data: list[float]):
#         nodes: list[Node] = []
#         self.__head: Node = None
#         self.__tail: Node = None
#         self.__current: Node = None
#
#         for item in data:
#             nodes.append(Node(item))
#
#         i = 0
#         while i < len(nodes):
#             if i == 0:
#                 self.__head = nodes[i]
#             if i == 1:
#                 self.__head.set_next(nodes[i])
#                 self.__head.next().set_prev(self.__head)
#             if i > 1:
#                 nodes[i-1].set_next(nodes[i])
#                 nodes[i].set_prev(nodes[i-1])
#             i += 1
#
#         length = len(nodes)
#         if length > 0:
#             self.__tail = nodes[length - 1]
#             if len(nodes) > 1:
#                 self.__tail.set_prev(nodes[length - 2])
#                 self.__tail.prev().set_next(self.__tail)
#
#     def __len__(self):
#         if self.__head is None:
#             return 0
#         count = 1
#         current = self.__head
#         while current.next() is not None:
#             current = current.next()
#             print("in len")
#             count += 1
#
#         return count
#
#     def __set_head(self, node: Node):
#         self.__head = node
#         self.__current = self.__head
#
#     def get_last(self):
#         current = self.__head
#         while current.next() is not None:
#             current = current.next()
#         return current
#
#     def append_node(self, node: Node):
#         if self.__head is None:
#             self.__set_head(node)
#             return
#         last = self.get_last()
#         last.set_next(node)
#         node.set_prev(last)
#
#     def append_data(self, data: float):
#         node = Node(data)
#         self.append_node(node)
#
#     def max(self):
#         max_ = float("-inf")
#         for node in self:
#             if node.data() > max_:
#                 max_ = node.data()
#         return max_
#
#     def min(self):
#         min_ = float("inf")
#         for node in self:
#             if node.data() < min_:
#                 min_ = node.data()
#         return min_
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         if self.__current is None:
#             self.__current = self.__head
#             raise StopIteration
#         curr = self.__current
#         self.__current = self.__current.next()
#         print("getting next")
#         return curr
#
#     def __getitem__(self, item):
#         if self.__head is None:
#             raise ValueError("LinkedList is empty")
#         if item == 0:
#             return self.__head
#
#         item: int
#         i = 0
#         current = self.__head
#         while i < item:
#             if current.next() is None:
#                 raise ValueError("index is beyond the end of LinkedList")
#             current = current.next()
#             i += 1
#         print("getting item at ", item)
#         return current
