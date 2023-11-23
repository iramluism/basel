from pathlib import Path
from unittest.mock import Mock

from basel.components import Component
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

    assert components == expected_components


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
                Component(name="component_A"),
                Component(name="component_B"),
                Component(name="component_C"),
                Component(name="component_D"),
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

    def mock_get_local_py_module(_import):
        return _import

    loader._get_local_py_module = mock_get_local_py_module

    loader.load_links()

    links = loader.get_links()

    assert links == expected_links
