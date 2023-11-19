from pathlib import Path
from typing import List

from basel.components import ModuleComponent
from basel.components import ModuleComponentLoader
import pytest

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
            ],
        ),
    ],
)
def test_get_py_module_component(root_module: Path, expected_py_modules: List[Path]):
    loader = ModuleComponentLoader()
    py_modules = loader.get_py_modules(root_module)

    assert py_modules == expected_py_modules


@pytest.mark.parametrize(
    "root_module,expected_components",
    [
        (
            root_stub_project,
            [
                ModuleComponent(
                    path=root_stub_project / Path("__init__.py"), name="stub_project"
                ),
                ModuleComponent(
                    path=root_stub_project / Path("module_1.py"), name="module_1"
                ),
                ModuleComponent(
                    path=root_stub_project / Path("package_a/module_a2.py"),
                    name="module_a2",
                ),
                ModuleComponent(
                    path=root_stub_project / Path("package_a/module_a1.py"),
                    name="module_a1",
                ),
                ModuleComponent(
                    path=root_stub_project / Path("package_a/__init__.py"),
                    name="package_a",
                ),
            ],
        ),
    ],
)
def test_load_components(root_module: Path, expected_components: List[ModuleComponent]):
    loader = ModuleComponentLoader()
    loader.load_components(root_module)

    assert loader.get_components() == expected_components


@pytest.mark.parametrize(
    "component,expected_abstraction",
    [
        (
            ModuleComponent(
                path=root_stub_project / Path("package_a/module_a1.py"),
                name="module_a1",
            ),
            1,
        ),
        (
            ModuleComponent(
                path=root_stub_project / Path("package_a/module_a2.py"),
                name="module_a2",
            ),
            0.5,
        ),
    ],
)
def tests_calculate_abstraction(
    component: ModuleComponent, expected_abstraction: float
):
    abstraction = component.get_abstraction()
    assert abstraction == expected_abstraction


@pytest.mark.parametrize(
    "component,expected_inestability",
    [
        (
            ModuleComponent(
                path=root_stub_project / Path("/module_1.py"),
                name="module_a1",
            ),
            1,
        ),
        (
            ModuleComponent(
                path=root_stub_project / Path("package_a/module_a2.py"),
                name="module_a2",
            ),
            0,
        ),
        (
            ModuleComponent(
                path=root_stub_project / Path("package_a/module_a1.py"),
                name="module_a2",
            ),
            0,
        ),
    ],
)
def tests_calculate_inestability(
    component: ModuleComponent, expected_inestability: float
):
    inestability = component.get_instability()
    assert inestability == expected_inestability
