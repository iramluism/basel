import abc

from basel.components.nodes import Node


class Link(metaclass=abc.ABCMeta):
    def __init__(self, source: Node, target: Node) -> None:
        self.source = source
        self.target = target

    def __eq__(self, other_link):
        return self.source == other_link.source and self.target == other_link.target
