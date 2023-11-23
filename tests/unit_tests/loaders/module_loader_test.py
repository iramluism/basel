import os
from pathlib import Path
from unittest.mock import Mock

from basel.components import Component
from basel.components.classes import ClassNode
from basel.components.links import Link
from basel.components.modules import ModuleNode
from basel.loaders.modules import ModuleLoader
from basel.parsers import Parser
import pytest

STUB_PROJECT_1_PATH = Path("tests/stubs/project_1")


@pytest.mark.parametrize(
    "paths,expected_components",
    [
        (
            [STUB_PROJECT_1_PATH],
            [
                Component(
                    name=str(STUB_PROJECT_1_PATH / "module_1.py"),
                    nodes=[
                        ModuleNode(
                            str(STUB_PROJECT_1_PATH / "module_1.py"),
                        )
                    ],
                ),
                Component(
                    name=str(STUB_PROJECT_1_PATH / "module_2.py"),
                    nodes=[
                        ModuleNode(
                            str(STUB_PROJECT_1_PATH / "module_2.py"),
                        )
                    ],
                ),
                Component(
                    name=str(STUB_PROJECT_1_PATH / "package_b/__init__.py"),
                    nodes=[
                        ModuleNode(
                            str(STUB_PROJECT_1_PATH / "package_b/__init__.py"),
                        )
                    ],
                ),
                Component(
                    name=str(STUB_PROJECT_1_PATH / "package_a/module_a1.py"),
                    nodes=[
                        ModuleNode(
                            str(STUB_PROJECT_1_PATH / "package_a/module_a1.py"),
                        )
                    ],
                ),
            ],
        )
    ],
)
def test_module_loader(paths, expected_components):
    mock_parser = Mock(spec=Parser)
    loader = ModuleLoader(mock_parser)

    loader.load_components(paths)

    components = loader.get_components()

    _components = set()
    for expected_comp in expected_components:
        for comp in components:
            if comp == expected_comp:
                _components.add(comp.name)

    assert len(_components) == len(expected_components)


@pytest.mark.parametrize(
    "components,_imports,expected_links",
    [
        (
            #
            #     A
            #    / \
            #   *   *
            #   B   C
            #   \   /
            #    * *
            #     C
            [
                Component(name="component_A", nodes=[ModuleNode("component_A")]),
                Component(name="component_B", nodes=[ModuleNode("component_B")]),
                Component(name="component_C", nodes=[ModuleNode("component_C")]),
                Component(name="component_D", nodes=[ModuleNode("component_D")]),
            ],
            {
                "component_A": ["component_B", "component_C"],
                "component_B": ["component_D"],
                "component_C": ["component_D"],
            },
            [
                Link(Component(name="component_A"), Component(name="component_B")),
                Link(Component(name="component_A"), Component(name="component_C")),
                Link(Component(name="component_B"), Component(name="component_D")),
                Link(Component(name="component_C"), Component(name="component_D")),
            ],
        )
    ],
)
def test_load_links(components, _imports, expected_links):
    mock_parser = Mock(spec=Parser)

    def mock_get_imports(path):
        return _imports.get(path, [])

    mock_parser.get_imports.side_effect = mock_get_imports

    loader = ModuleLoader(mock_parser, components)

    def mock_search_py_module(_import):
        return _import

    loader.search_py_module = mock_search_py_module

    loader.load_links()

    links = loader.get_links()

    assert links == expected_links


@pytest.mark.parametrize(
    "root,_import,expected_py_module",
    [
        (
            STUB_PROJECT_1_PATH,
            "package_a.module_a1",
            Path("package_a/module_a1.py"),
        ),
        (
            STUB_PROJECT_1_PATH,
            "package_a.module_a1.ConcretClass",
            Path("package_a/module_a1.py"),
        ),
        (STUB_PROJECT_1_PATH, "package_a", Path("package_a")),
        (STUB_PROJECT_1_PATH, "package_b", Path("package_b/__init__.py")),
        (STUB_PROJECT_1_PATH, "dataclasses.dataclass", None),
    ],
)
def test_search_by_module(root, _import, expected_py_module):
    cwd = os.getcwd()
    os.chdir(root)

    mock_parser = Mock(spec=Parser)

    loader = ModuleLoader(mock_parser)

    py_module = loader.search_py_module(_import)

    os.chdir(cwd)

    assert py_module == expected_py_module


@pytest.mark.parametrize(
    "components,_classes,expected_components",
    [
        (
            (
                Component(name="Component_A", nodes=[ModuleNode("Module_A")]),
                Component(name="Component_B", nodes=[ModuleNode("Module_B")]),
            ),
            {
                "Module_A": [("ClassA", [], {})],
                "Module_B": [("ClassB", ["ClassA"], {})],
            },
            [
                Component(
                    name="Component_A",
                    nodes=[ModuleNode("Module_A", children=[ClassNode("ClassA")])],
                ),
                Component(
                    name="Component_B",
                    nodes=[
                        ModuleNode(
                            "Module_B", children=[ClassNode("ClassB", ["ClassA"])]
                        )
                    ],
                ),
            ],
        )
    ],
)
def test_load_classes(components, _classes, expected_components):
    mock_parser = Mock(spec=Parser)

    def mock_get_parsed_classes(module):
        return _classes.get(module)

    mock_parser.get_classes.side_effect = mock_get_parsed_classes

    loader = ModuleLoader(mock_parser, components)

    loader.load_classes()

    components = loader.get_components()

    assert components == expected_components


@pytest.mark.parametrize(
    "components,links,expected_instability",
    [
        (
            #
            #     A
            #    / \
            #   *   *
            #   B   C
            #   \   /
            #    * *
            #     C
            [
                Component(name="component_A"),
                Component(name="component_B"),
                Component(name="component_C"),
                Component(name="component_D"),
            ],
            [
                Link(Component(name="component_A"), Component(name="component_B")),
                Link(Component(name="component_A"), Component(name="component_C")),
                Link(Component(name="component_B"), Component(name="component_D")),
                Link(Component(name="component_C"), Component(name="component_D")),
            ],
            {
                "component_A": 1,
                "component_B": 0.5,
                "component_C": 0.5,
                "component_D": 0,
            },
        ),
        (
            # A --* B
            # C Isolated Component
            [
                Component(name="component_A"),
                Component(name="component_B"),
                Component(name="component_C"),
            ],
            [
                Link(Component(name="component_A"), Component(name="component_B")),
            ],
            {
                "component_A": 1,
                "component_B": 0,
                "component_C": 1,
            },
        ),
        (
            # A *--* B Circular Dependency
            [
                Component(name="component_A"),
                Component(name="component_B"),
            ],
            [
                Link(Component(name="component_A"), Component(name="component_B")),
                Link(Component(name="component_B"), Component(name="component_A")),
            ],
            {
                "component_A": 0.5,
                "component_B": 0.5,
            },
        ),
    ],
)
def test_calculate_instability(components, links, expected_instability):
    mock_parser = Mock(spec=Parser)

    loader = ModuleLoader(mock_parser, components, links)

    loader.calculate_instability()

    for comp_name, instability in expected_instability.items():
        comp = loader.get_component(comp_name)
        assert comp.instability == instability
