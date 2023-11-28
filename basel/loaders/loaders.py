import abc
from typing import Dict
from typing import List
from typing import Optional

from basel.components import Component
from basel.components.links import Link
from basel.parsers.parser import Parser


class Loader(metaclass=abc.ABCMeta):
    components: Dict[str, Component]

    def __init__(
        self,
        parser: Parser,
        components: Optional[List[Component]] = None,
        links: List[Link] = None,
    ) -> None:
        self.links = links or []
        self.parser = parser
        self.components = {}

        for comp in components or []:
            self.add_component(comp)

    @abc.abstractmethod
    def load_components(self, *args, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def load_links(self, *args, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate_error(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate_instability(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate_abstraction(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate_mean_error(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate_mean_abstraction(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate_mean_instability(self):
        raise NotImplementedError()

    def get_component(self, component_name):
        return self.components.get(component_name)

    def get_components(self):
        return list(self.components.values())

    def add_component(self, component: Component):
        self.components[component.name] = component

    def link_component(self, source, target):
        link = Link(source, target)
        self.links.append(link)

    def get_links(self):
        return self.links
