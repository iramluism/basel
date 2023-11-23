import os
from pathlib import Path
from typing import List

from basel import utils
from basel.components import Component
from basel.components.classes import ClassNode
from basel.components.modules import ModuleNode
from basel.loaders import Loader


class ModuleLoader(Loader):
    def load_components(self, paths: List[str]):
        modules = self._discover_modules(paths)
        self.add_modules(modules)

    def _search_linked_component(self, module_path):
        for comp in self.components.values():
            if comp.has_node(module_path):
                return comp

    def _get_imports_from_component_nodes(self, component):
        _imports = []
        for node in component:
            _imports.extend(self.parser.get_imports(node.name))

        return _imports

    def load_links(self):
        for comp_name, comp in self.components.items():
            comp_imports = self._get_imports_from_component_nodes(comp)
            for _import in comp_imports:
                module_path = self.search_py_module(_import)
                linked_component = self._search_linked_component(str(module_path))
                if linked_component:
                    self.link_component(comp, linked_component)

    def _format_to_py_module_path(self, _import: str):
        return Path(_import.replace(".", "/") + ".py")

    def _format_to_py_package_path(self, _import: str):
        return Path(_import.replace(".", "/")) / "__init__.py"

    def search_py_module(self, _import: str):
        _parent_import = ".".join(_import.split(".")[:-1])
        search_attemps = [_import, _parent_import]

        for _import in search_attemps:
            module = self._get_local_py_module(_import)
            if module:
                return module

    def _load_classes_for_node(self, node):
        _classes = self.parser.get_classes(node.name)
        for _class in _classes:
            class_node = ClassNode(*_class)
            node.add_child(class_node)

    def load_classes(self):
        for comp_name, comp in self.components.items():
            for node in comp:
                self._load_classes_for_node(node)

    def _get_input_and_output_deps_of_component(self, component):
        input_deps = output_deps = 0

        for link in self.links:
            if link.source.name == component.name:
                output_deps += 1
            elif link.target.name == component.name:
                input_deps += 1

        return input_deps, output_deps

    def calculate_instability(self):
        for comp in self.components.values():
            input_deps, output_deps = self._get_input_and_output_deps_of_component(comp)
            comp_instability = utils.instability(input_deps, output_deps)
            comp.set_instability(comp_instability)

    def _get_local_py_module(self, _import: str):
        py_module = self._format_to_py_module_path(_import)
        if os.path.exists(py_module):
            return py_module

        py_package = self._format_to_py_package_path(_import)
        if os.path.exists(py_package):
            return py_package

        if os.path.isdir(py_package.parent):
            return py_package.parent

    def add_modules(self, modules: List[Path]):
        for module_path in modules:
            module_name = str(module_path)
            module_node = ModuleNode(name=module_name)
            component = Component(name=module_name, nodes=[module_node])

            self.add_component(component)

    def _discover_modules(self, paths: List[str]):
        discovered_modules = []

        for path in paths:
            for root, packages, modules in os.walk(path):
                for module in sorted(modules):
                    if not module.endswith(".py"):
                        continue

                    module_path = Path(root) / module
                    discovered_modules.append(module_path)

        return discovered_modules
