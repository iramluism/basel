import abc 
import os 

from pathlib import Path

from typing import Optional, NoReturn, List, Union
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
    
    @abc.abstractmethod    
    def calculate_abstraction(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def calculate_stability(self):
        raise NotImplementedError()


class ComponentLoader(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def load_components(self, *args, **kwargs) -> Component:
        raise NotImplementedError()
    

class ModuleComponent(Component):
    name: Optional[str] = None
    path: Optional[Path] = None 
    
    def __init__(self, path: Path, name: Optional[str]=None):
        if not name:
            name = self._get_name_from_path(path)
        
        self.path = path 
        self.name = name
        
    @staticmethod
    def _get_name_from_path(path: Path):
        if "__init__.py" == path.name:
            package = os.path.dirname(path)
            return os.path.split(package)[-1]
            
        else:
            return path.stem 
        
    
    def calculate_abstraction(self):
        pass 
    
    def calculate_stability(self):
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
