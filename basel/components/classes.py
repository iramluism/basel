from typing import Dict
from typing import List
from typing import Optional

from basel.components.nodes import Node


class ClassNode(Node):
    def __init__(
        self,
        name: str,
        subclasses: Optional[List] = None,
        keywords: Optional[Dict] = None,
        **kwargs,
    ):
        super().__init__(name, **kwargs)
        self.subclasses = subclasses or []
        self.keywords = keywords or {}

    def __eq__(self, other_node):
        if not other_node:
            return False

        match_names = other_node.name == self.name
        match_subclasses = other_node.subclasses == self.subclasses
        match_keywords = other_node.keywords == self.keywords
        match_children = self.has_children(other_node)

        return match_names and match_children and match_keywords and match_subclasses
