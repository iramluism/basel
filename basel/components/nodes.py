class Node:
    def __init__(self, name, children=None) -> None:
        self.name = name
        self.children = children or {}

    def add_child(self, node):
        self.children[node.name] = node

    def get_child(self, node_name):
        return self.children.get(node_name)

    def remove_child(self, node_name):
        self.children.pop(node_name)
