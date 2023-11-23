import abc
from typing import List

from basel.components.nodes import Node


class Component(metaclass=abc.ABCMeta):
    def __init__(self, name: str, nodes: List[Node] = None) -> None:
        self.name = name
        self.nodes = {}
        self.instability = 1
        self.abstraction = 1

        for node in nodes or []:
            self.add_node(node)

    def set_instability(self, instability):
        self.instability = instability

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
        if not component:
            return False

        equal_names = self.name == component.name

        for other_node in component:
            self_node = self.get_node(other_node.name)
            if other_node != self_node:
                return False

        return equal_names

    def __ne__(self, component):
        return not self.__eq__(component)
