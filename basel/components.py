import abc
import ast
from collections import namedtuple
from dataclasses import dataclass
import importlib
import inspect
import os
from pathlib import Path
from typing import Dict
from typing import List
from typing import NoReturn
from typing import Optional

ASPoint = namedtuple("ASPoint", ["x", "y"])


@dataclass
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


class ModuleComponent(Component):
    name: Optional[str] = None
    path: Optional[Path] = None

    def __init__(
        self, path: Optional[Path] = None, name: Optional[str] = None, *args, **kwargs
    ):
        super().__init__(self, *args, **kwargs)
        if path and not name:
            name = self._get_name_from_path(path)

        if name and not path:
            path = self._get_path_from_name(name)

        self.path = path
        self.name = name

    @staticmethod
    def _is_abstract_class(_class):
        return inspect.isabstract(_class)

    @staticmethod
    def _get_path_from_name(name: str):
        obj = importlib.import_module(name)
        module_path = name.replace(".", "/")
        if inspect.ismodule(obj):
            path = f"{module_path}.py"
        else:
            path = f"{module_path}/__init__.py"

        return Path(path)

    @staticmethod
    def _get_name_from_path(path: Path):
        parent_name = str(path.parent).replace("/", ".")

        if "__init__.py" == path.name:
            return parent_name
        else:
            return f"{parent_name}.{path.stem}"

    def get_abstraction(self):
        self.load_classes()
        self.calculate_abstraction()
        return self.abstraction

    def depend_of(self, component_name: str):
        for component in self.external_dependencies:
            if component.name == component_name:
                return True

        return False

    def load_classes(self):
        if self.no_abstract_classes or self.abstract_classes:
            return None

        module = importlib.import_module(self.name)
        for module_name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and not self.depend_of(obj.__module__):
                self.add_class(
                    _class=obj,
                    is_abstract=self._is_abstract_class(obj),
                )

    def get_dependencies(self):
        with open(self.path, "r") as archivo:
            tree_imports = ast.parse(archivo.read())

        _imports = set()

        for node in ast.walk(tree_imports):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    _imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                modules = set()

                for alias in node.names:
                    try:
                        module_path = f"{node.module}.{alias.name}"
                        importlib.import_module(module_path)
                        modules.add(module_path)
                    except ImportError:
                        pass

                _imports = _imports | modules
                if len(modules) != len(node.names):
                    _imports.add(node.module)

        return _imports

    def load_dependencies(self, ignore_dependencies: Optional[List[str]] = None):
        if self.external_dependencies:
            return None

        dependencies = self.get_dependencies()

        for module in dependencies:
            if ignore_dependencies and module in ignore_dependencies:
                continue

            dep_comp = ModuleComponent(name=module)
            self.add_dependency(dep_comp)

    def get_instability(self, ignore_dependencies: Optional[List[str]] = None) -> float:
        self.calculate_instability()
        return self.instability


class ModuleComponentLoader(ComponentLoader):
    def __init__(
        self,
        root_path=None,
        components: Optional[Dict[str, ModuleComponent]] = None,
        ignore_dependencies: Optional[List[str]] = None,
    ):
        self.root_path = root_path
        self.components = components or {}
        self.ignore_dependencies = ignore_dependencies

    def load_components(self, root_path: Optional[Path] = None) -> NoReturn:
        if not root_path:
            root_path = self.root_path

        self._load_components(root_path)
        self._load_dependencies()
        self._load_classes()

    def _load_components(self, root_path):
        for module in self.get_py_modules(root_path):
            component = ModuleComponent(path=module)
            self.components[component.name] = component

    def _load_classes(self):
        for component in self.components.values():
            component.load_classes()

    def _load_dependencies(self):
        for component_name, component in self.components.items():
            component.load_dependencies(ignore_dependencies=self.ignore_dependencies)
            self.components[component_name] = component
            for comp_ext_deps in component.external_dependencies:
                if comp_ext_deps.name in self.components:
                    comp_deps = self.components.get(comp_ext_deps.name)
                    comp_deps.add_dependency(component, is_internal=True)

    def _find_py_modules(self, root, modules) -> List[Path]:
        py_modules = []
        for module in modules:
            if not module.endswith(".py"):
                continue

            module_path = Path(os.path.join(root, module))
            py_modules.append(module_path)

        return py_modules

    def get_as_plane(self) -> Dict[str, ASPoint]:
        as_plane = {}
        for component_name, component in self.components.items():
            instability = component.get_instability()
            abstraction = component.get_abstraction()
            as_point = ASPoint(x=instability, y=abstraction)

            as_plane[component_name] = as_point

        return as_plane

    def calculate_main_distance(self):
        main_distance = 0
        distances = []

        for component_name, component in self.components.items():
            comp_distance = component.get_distance()
            distances.append(comp_distance)

        if distances:
            main_distance = sum(distances) / len(distances)

        return main_distance

    def get_py_modules(self, root_path: str):
        py_modules = []

        for root, packages, modules in os.walk(root_path, topdown=True):
            if "__init__.py" not in modules:
                continue

            py_modules.extend(self._find_py_modules(root, modules))

        return py_modules

    def get_components(self) -> List[ModuleComponent]:
        return list(self.components.values())
