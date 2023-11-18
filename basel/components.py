import abc 
import os 

from pathlib import Path

from typing import Optional, NoReturn, List
from dataclasses import dataclass


@dataclass
class Component(metaclass=abc.ABCMeta):
    abstraction: Optional[float] = None
    inestability: Optional[float] = None 
    
    external_dependencies: float = 0.0 
    internal_dependencies: float = 0.0 
    
    no_abstract_classes: float = 0.0 
    abstract_classes: float = 0.0 
    
    def add_dependency(self, is_internal=False) -> NoReturn:
        if is_internal:
            self.internal_dependencies += 1 
        else: 
            self.external_dependencies += 1
    
    def add_class(self, is_abstract=True) -> NoReturn: 
        if is_abstract:
            self.abstract_classes += 1 
        else:
            self.no_abstract_classes += 1


class ComponentLoader(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def load_component(self, *args, **kwargs) -> Component:
        raise NotImplementedError()


@dataclass
class ModuleComponent(Component):
    module_name: Optional[str] = None
    path: Optional[str] = None 


class ModuleComponentLoader(ComponentLoader):
    
    components = []
    
    def load_component(self, root_path: str) -> ModuleComponent:
        
        self.get_py_modules(root_path)
        
    
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
