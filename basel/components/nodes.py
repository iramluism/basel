class Node:
    def __init__(self, name, children=None) -> None:
        self.name = name
        self.children = {}

        for child in children or []:
            self.add_child(child)

    def add_child(self, node):
        self.children[node.name] = node

    def get_children(self):
        return list(self.children.values())

    def get_child(self, node_name):
        return self.children.get(node_name)

    def remove_child(self, node_name):
        self.children.pop(node_name)

    def __eq__(self, other_node):
        if not other_node:
            return False

        match_names = other_node.name == self.name
        match_children = self.has_children(other_node)

        return match_names and match_children

    def has_children(self, children):
        for other_child in children:
            self_child = self.get_child(other_child.name)
            if self_child != other_child:
                return False

        return True

    def __ne__(self, other_node):
        return not self.__eq__(other_node)

    def __iter__(self):
        for child in self.children.values():
            yield child

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.name}>"
