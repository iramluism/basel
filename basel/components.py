import abc
from dataclasses import dataclass
import importlib
import inspect
import os
from pathlib import Path
from typing import List
from typing import NoReturn
from typing import Optional


@dataclass
class Component(metaclass=abc.ABCMeta):
    def __init__(
        self,
        abstraction: Optional[float] = None,
        instability: Optional[float] = None,
        external_dependencies: Optional[float] = None,
        internal_dependencies: Optional[float] = None,
        no_abstract_classes: Optional[float] = None,
        abstract_classes: Optional[float] = None,
    ):
        self.abstraction = abstraction
        self.instability = instability

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
    def get_abstraction(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_instability(self):
        raise NotImplementedError()

    def calculate_abstraction(self):
        abstraction = 1
        n_abstract_classess = len(self.abstract_classes)
        n_classes = len(self.abstract_classes) + len(self.no_abstract_classes)

        if n_classes:
            abstraction = n_abstract_classess / n_classes

        self.abstraction = abstraction
        return abstraction

    def calculate_instability(self):
        raise NotImplementedError()


class ComponentLoader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load_components(self, *args, **kwargs) -> Component:
        raise NotImplementedError()


class ModuleComponent(Component):
    name: Optional[str] = None
    path: Optional[Path] = None

    def __init__(self, path: Path, name: Optional[str] = None, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        if not name:
            name = self._get_name_from_path(path)

        self.path = path
        self.name = name

    @staticmethod
    def _is_abstract_class(_class):
        return inspect.isabstract(_class)

    @staticmethod
    def _get_name_from_path(path: Path):
        if "__init__.py" == path.name:
            package = os.path.dirname(path)
            return os.path.split(package)[-1]

        else:
            return path.stem

    def get_abstraction(self):
        for module_class in self._get_classes():
            self.add_class(
                _class=module_class,
                is_abstract=self._is_abstract_class(module_class),
            )

        self.calculate_abstraction()
        return self.abstraction

    def _get_classes(self):
        classes = []
        package_path = str(self.path.parent).replace("/", ".")
        module_path = f"{package_path}.{self.name}"

        module = importlib.import_module(module_path)
        for module_name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                classes.append(obj)

        return classes

    def get_instability(self):
        pass


class ModuleComponentLoader(ComponentLoader):
    def __init__(self, root_path=None):
        self.root_path = root_path
        self.components = {}

    def load_components(self, root_path: str) -> NoReturn:
        if root_path in self.components:
            return None

        for module in self.get_py_modules(root_path):
            component = ModuleComponent(path=module)
            self.components[str(module)] = component

    def _find_py_modules(self, root, modules) -> List[Path]:
        py_modules = []
        for module in modules:
            if not module.endswith(".py"):
                continue

            module_path = Path(os.path.join(root, module))
            py_modules.append(module_path)

        return py_modules

    def get_py_modules(self, root_path: str):
        py_modules = []

        for root, packages, modules in os.walk(root_path, topdown=True):
            if "__init__.py" not in modules:
                continue

            py_modules.extend(self._find_py_modules(root, modules))

        return py_modules

    def get_components(self) -> List[ModuleComponent]:
        return list(self.components.values())
