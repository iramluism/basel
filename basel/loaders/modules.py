import os
from pathlib import Path
from typing import List

from basel.components import Component
from basel.components.modules import ModuleNode
from basel.loaders import Loader


class ModuleLoader(Loader):
    def load_components(self, paths: List[str]):
        modules = self._discover_modules(paths)
        print(modules)
        self.add_modules(modules)

    def add_modules(self, modules: List[Path]):
        for module_path in modules:
            module_name = str(module_path)
            module_node = ModuleNode(name=module_name)
            component = Component(name=module_name, nodes=[module_node])

            self.add_component(component)

    def _discover_modules(self, paths: List[str]):
        discovered_modules = []

        for path in paths:
            for root, packages, modules in os.walk(path, topdown=True):
                for module in modules:
                    if not module.endswith(".py"):
                        continue

                    module_path = Path(root) / module
                    discovered_modules.append(module_path)

        return discovered_modules
