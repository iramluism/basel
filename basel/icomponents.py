import abc
from typing import Dict
from typing import List
from typing import NoReturn
from typing import Optional

from basel.dtos import ASPoint


class Component(metaclass=abc.ABCMeta):
    def __init__(
        self,
        abstraction: Optional[float] = None,
        instability: Optional[float] = None,
        distance: Optional[float] = None,
        external_dependencies: Optional[float] = None,
        internal_dependencies: Optional[float] = None,
        no_abstract_classes: Optional[float] = None,
        abstract_classes: Optional[float] = None,
    ):
        self.abstraction = abstraction or 1
        self.instability = instability or 1
        self.distance = distance or 0

        self.external_dependencies = external_dependencies or []
        self.internal_dependencies = internal_dependencies or []

        self.no_abstract_classes = no_abstract_classes or []
        self.abstract_classes = abstract_classes or []

    def add_dependency(self, component, is_internal=False) -> NoReturn:
        if is_internal:
            self.internal_dependencies.append(component)
        else:
            self.external_dependencies.append(component)

    def add_class(self, _class, is_abstract=True) -> NoReturn:
        if is_abstract:
            self.abstract_classes.append(_class)
        else:
            self.no_abstract_classes.append(_class)

    @abc.abstractmethod
    def get_dependencies(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_abstraction(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_instability(self, ignore_dependencies: Optional[List[str]] = None) -> float:
        raise NotImplementedError()

    def get_distance(self) -> float:
        return self.distance

    def calculate_distance(self):
        abstraction = self.abstraction
        instability = self.instability

        distance = abs(abstraction + instability - 1)

        self.distance = distance

        return self.distance

    def calculate_abstraction(self):
        abstraction = 1
        n_abstract_classess = len(self.abstract_classes)
        n_classes = len(self.abstract_classes) + len(self.no_abstract_classes)

        if n_classes:
            abstraction = n_abstract_classess / n_classes

        self.abstraction = abstraction
        return abstraction

    def calculate_instability(self):
        instability = 1
        n_external_deps = len(self.external_dependencies)
        n_deps = n_external_deps + len(self.internal_dependencies)

        if n_deps:
            instability = n_external_deps / n_deps

        self.instability = instability
        return instability


class ComponentLoader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load_components(self, *args, **kwargs) -> Component:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_as_plane(self) -> Dict[str, ASPoint]:
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate_main_distance(self) -> float:
        raise NotImplementedError()
