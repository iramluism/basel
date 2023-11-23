import abc
from typing import List

from basel.components.nodes import Node


class Component(metaclass=abc.ABCMeta):
    def __init__(self, name: str, nodes: List[Node] = None) -> None:
        self.name = name
        self.nodes = {}

        for node in nodes or []:
            self.add_node(node)

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.name}>"

    def has_node(self, node_name):
        return node_name in self.nodes

    def add_node(self, node: Node):
        self.nodes[node.name] = node

    def get_node(self, node_name):
        return self.nodes.get(node_name)

    def __iter__(self):
        for node in self.nodes.values():
            yield node

    def __eq__(self, component):
        equal_names = self.name == component.name

        for other_node in component.nodes:
            self_node = self.get_node(other_node)
            if not self_node:
                return False

        return equal_names
