from pathlib import Path
from unittest.mock import Mock

from basel.components import Component
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
