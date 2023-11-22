from pathlib import Path
from typing import List

from basel.components import ModuleComponentLoader
from basel.components.modules import ModuleComponent
import pytest

root_stub_project = Path("tests/stubs/stub_project")


@pytest.mark.skip
@pytest.mark.parametrize(
    "root_module,expected_py_modules",
    [
        (
            root_stub_project,
            [
                root_stub_project / Path("__init__.py"),
                root_stub_project / Path("module_1.py"),
                root_stub_project / Path("package_b/module_b1.py"),
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


@pytest.mark.skip
@pytest.mark.parametrize(
    "root_module,expected_components,exclude_components,exclude_packages",
    [
        (
            root_stub_project,
            [
                ModuleComponent(
                    path=root_stub_project / Path("__init__.py"),
                ),
                ModuleComponent(
                    path=root_stub_project / Path("module_1.py"),
                ),
                ModuleComponent(
                    path=root_stub_project / Path("package_b/module_b1.py"),
                ),
                ModuleComponent(
                    path=root_stub_project / Path("package_a/module_a2.py"),
                ),
                ModuleComponent(
                    path=root_stub_project / Path("package_a/module_a1.py"),
                ),
                ModuleComponent(
                    path=root_stub_project / Path("package_a/__init__.py"),
                    name="tests.stubs.stub_project.package_a",
                ),
            ],
            None,
            False,
        ),
        (
            root_stub_project,
            [
                ModuleComponent(
                    path=root_stub_project / Path("module_1.py"),
                ),
                ModuleComponent(
                    path=root_stub_project / Path("package_b/module_b1.py"),
                ),
                ModuleComponent(
                    path=root_stub_project / Path("package_a/module_a2.py"),
                ),
                ModuleComponent(
                    path=root_stub_project / Path("package_a/module_a1.py"),
                ),
            ],
            None,
            True,
        ),
        (
            root_stub_project,
            [
                ModuleComponent(
                    path=root_stub_project / Path("module_1.py"),
                ),
                ModuleComponent(
                    path=root_stub_project / Path("package_b/module_b1.py"),
                ),
                ModuleComponent(
                    path=root_stub_project / Path("package_a/module_a1.py"),
                ),
                ModuleComponent(
                    path=root_stub_project / Path("package_a/__init__.py"),
                ),
            ],
            [
                "tests/stubs/stub_project/__init__.py",
                "tests/stubs/stub_project/package_a/module_a2.py",
            ],
            False,
        ),
    ],
)
def test_load_components(
    root_module: Path,
    expected_components: List[ModuleComponent],
    exclude_components: List[str],
    exclude_packages: bool,
):
    loader = ModuleComponentLoader()
    loader.load_components(
        root_module,
        exclude_components=exclude_components,
        exclude_packages=exclude_packages,
    )

    components = loader.get_components()
    for component, expected_component in zip(components, expected_components):
        assert component.path == expected_component.path
        assert component.name == expected_component.name


@pytest.mark.parametrize(
    "component,expected_abstraction",
    [
        (
            ModuleComponent(
                path=root_stub_project / Path("package_a/module_a1.py"),
            ),
            1,
        ),
        (
            ModuleComponent(
                path=root_stub_project / Path("package_a/module_a2.py"),
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
                path=root_stub_project / Path("module_1.py"),
            ),
            1,
        ),
        (
            ModuleComponent(
                path=root_stub_project / Path("package_a/module_a2.py"),
                internal_dependencies=[
                    ModuleComponent(path=root_stub_project / Path("module_1.py"))
                ],
            ),
            0,
        ),
        (
            ModuleComponent(
                path=root_stub_project / Path("package_a/module_a1.py"),
                internal_dependencies=[
                    ModuleComponent(path=root_stub_project / Path("module_1.py"))
                ],
            ),
            0,
        ),
    ],
)
def tests_calculate_inestability(
    component: ModuleComponent, expected_inestability: float
):
    inestability = component.get_instability(ignore_dependencies=["abc"])
    assert inestability == expected_inestability
