import ast
import importlib
import os
from pathlib import Path
from typing import Dict
from typing import List
from typing import NoReturn
from typing import Optional

from basel.dtos import ASPoint
from basel.icomponents import Component
from basel.icomponents import ComponentLoader


class ModuleComponent(Component):
    name: Optional[str] = None
    path: Optional[Path] = None
    package_module = "__init__.py"

    def __init__(
        self,
        root_path: Optional[Path] = None,
        path: Optional[Path] = None,
        name: Optional[str] = None,
        *args,
        **kwargs,
    ):
        super().__init__(self, *args, **kwargs)

        self.path = path
        self.root_path = root_path
        self.name = str(path)

    def is_package(self):
        return self.path.match(self.package_module)

    def get_abstraction(self):
        self.load_classes()
        self.calculate_abstraction()
        return self.abstraction

    def depend_of(self, component_name: str):
        for component in self.external_dependencies:
            if component.name == component_name:
                return True

        return False

    @staticmethod
    def _import_module(module_path):
        try:
            module = importlib.import_module(module_path)
            return module
        except ImportError:
            pass

    def _get_import_path(self, _import):
        mod_path = _import.replace(".", "/") + ".py"
        abs_path = os.path.abspath(mod_path)
        if os.path.exists(abs_path):
            return Path(abs_path).relative_to(os.getcwd())

        return _import

    def _eval_dependency(self, dep) -> set:
        _imports = set()

        if isinstance(dep, ast.Import):
            for alias in dep.names:
                _imports.add(self._get_import_path(alias.name))
        elif isinstance(dep, ast.ImportFrom):
            modules = set()

            for alias in dep.names:
                module_path = f"{dep.module}.{alias.name}"
                module = self._import_module(module_path)
                if module:
                    modules.add(self._get_import_path(module_path))

            _imports = _imports | modules
            if len(modules) != len(dep.names):
                _imports.add(self._get_import_path(dep.module))

        return _imports

    def get_dependencies(self):
        with open(self.path, "r") as archivo:
            tree_imports = ast.parse(archivo.read())

        _imports = set()
        for node in ast.walk(tree_imports):
            deps = self._eval_dependency(node)
            _imports = _imports | deps

        return _imports

    def load_classes(self):
        with open(self.path, "r") as archivo:
            ast_tree = ast.parse(archivo.read())

        _imports = set()
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.ClassDef):
                self.add_class(node, is_abstract=self._is_abstract_class(node))

        return _imports

    def _is_abstract_class(self, _class: ast.ClassDef):
        for keyword in _class.keywords:
            if keyword.arg == "metaclass" and keyword.value.attr == "ABCMeta":
                return True

        for base in _class.bases:
            if hasattr(base, "id") and base.id == "ABC":
                return True

            if hasattr(base, "attr") and base.attr in ["ABC", "ABCMeta"]:
                return True

        return False

    def load_dependencies(self, ignore_dependencies: Optional[List[str]] = None):
        if self.external_dependencies:
            return None

        dependencies = self.get_dependencies()

        for module in dependencies:
            if ignore_dependencies and module in ignore_dependencies:
                continue

            dep_comp = ModuleComponent(root_path=self.root_path, path=module)
            self.add_dependency(dep_comp)

    def get_instability(self, ignore_dependencies: Optional[List[str]] = None) -> float:
        self.calculate_instability()
        return self.instability


class ModuleComponentLoader(ComponentLoader):
    components: Dict[str, ModuleComponent]

    def __init__(self, root_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root_path = root_path
        self._ignore_native_library()

    def _ignore_native_library(self):
        self.ignore_deps(["abc", "typing"])

    def load_components(
        self,
        root_path: Optional[Path] = None,
        ignore_dependencies: Optional[List[str]] = None,
        exclude_components: Optional[List[str]] = None,
        exclude_packages: bool = False,
    ) -> NoReturn:
        if not root_path:
            root_path = self.root_path

        self._load_components(root_path)
        self._remove_components(exclude_components, exclude_packages)
        self.ignore_deps(exclude_components or [])
        self._load_dependencies(ignore_dependencies)
        self._load_classes()

    def _remove_components(
        self,
        rules: Optional[List[str]] = None,
        exclude_packages: bool = False,
    ):
        if not rules:
            rules = []

        if exclude_packages:
            rules.append("__init__.py")

        for comp_name, comp in list(self.components.items()):
            comp = self.components[comp_name]

            if any(comp.path.match(rule) for rule in rules):
                self.components.pop(comp_name)

    def _load_components(self, root_path):
        for module in self.get_py_modules(root_path):
            component = ModuleComponent(
                path=module,
                root_path=root_path,
            )
            self.components[component.name] = component

    def _load_classes(self):
        for component in self.components.values():
            component.load_classes()

    def _load_dependencies(self, ignore_dependencies: Optional[List[str]] = None):
        if not ignore_dependencies:
            ignore_dependencies = []

        ignore_dependencies += self.ignore_dependencies

        for component_name, component in self.components.items():
            component.load_dependencies(ignore_dependencies=ignore_dependencies)
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
            distance = component.get_distance()
            as_point = ASPoint(x=instability, y=abstraction, d=distance)

            as_plane[component_name] = as_point

        return as_plane

    def calculate_main_distance(self, decimals: int = 2):
        main_distance = 0
        distances = []

        for component_name, component in self.components.items():
            comp_distance = component.get_distance()
            distances.append(comp_distance)

        if distances:
            main_distance = sum(distances) / len(distances)

        return round(main_distance, decimals)

    def get_py_modules(self, root_path: str):
        py_modules = []

        for root, packages, modules in os.walk(root_path, topdown=True):
            py_modules.extend(self._find_py_modules(root, modules))

        return py_modules

    def get_components(self) -> List[ModuleComponent]:
        return list(self.components.values())
