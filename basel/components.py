import abc
import ast
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
    def get_instability(self, ignore_dependencies: Optional[List[str]] = None) -> float:
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
        if "__init__.py" == path.name:
            package = os.path.dirname(path)
            return os.path.split(package)[-1]

        parent_name = str(path.parent).replace("/", ".")
        name = f"{parent_name}.{path.stem}"

        return name

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

    def _get_dependencies(self):
        with open(self.path, "r") as archivo:
            tree_imports = ast.parse(archivo.read())

        _imports = set()

        for node in ast.walk(tree_imports):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    _imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                _imports.add(node.module)

        return _imports

    def get_instability(self, ignore_dependencies: Optional[List[str]] = None) -> float:
        dependencies = self._get_dependencies()

        for module in dependencies:
            if ignore_dependencies and module in ignore_dependencies:
                continue

            dep_comp = ModuleComponent(name=module)
            self.add_dependency(dep_comp)

        self.calculate_instability()
        return self.instability


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
