
from pathlib import Path 
from typing import List
import pytest


from basel.components import ModuleComponentLoader

root_stub_project = Path("tests/stubs/stub_project")


@pytest.mark.parametrize(
    "root_module,expected_py_modules",
    [
        (
            root_stub_project, 
            [
                root_stub_project / Path("__init__.py"),
                root_stub_project / Path("module_1.py"),
                root_stub_project / Path("package_a/module_a2.py"),
                root_stub_project / Path("package_a/module_a1.py"),
                root_stub_project / Path("package_a/__init__.py"),
            ]
        ),
    ]
)
def test_get_py_module_component(root_module: Path, expected_py_modules: List[Path]):
    loader = ModuleComponentLoader()
    py_modules = loader.get_py_modules(root_module)

    assert py_modules == expected_py_modules
    