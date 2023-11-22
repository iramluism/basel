import abc
from typing import List

from basel.components.nodes import Node


class Component(metaclass=abc.ABCMeta):
    def __init__(self, name: str, nodes: List[Node]) -> None:
        self.name = name
        self.nodes = nodes

    def __eq__(self, component):
        print("HOLLLLAAA", self.name, component.name)
        return self.name == component.name
