import abc
from typing import List
from typing import Optional

from basel.components import Component


class Loader(metaclass=abc.ABCMeta):
    def __init__(self, components: Optional[List[Component]] = None) -> None:
        self.components = components or {}

    @abc.abstractmethod
    def load_components(self, *args, **kwargs):
        raise NotImplementedError()

    def get_component(self, component_name):
        return self.components.get(component_name)

    def get_components(self):
        return list(self.components.values())

    def add_component(self, component: Component):
        self.components[component.name] = component
