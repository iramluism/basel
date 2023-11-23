from pathlib import Path

from basel.parsers.python_parser import PythonParser
import pytest

STUB_PROJECT_1_PATH = Path("tests/stubs/project_1")


@pytest.mark.parametrize(
    "path,expected_imports",
    [
        (
            STUB_PROJECT_1_PATH / "module_1.py",
            [
                "abc",
                "abc.ABCMeta",
                "dataclasses.dataclass",
                "module_2",
                "package_a.module_a1.ConcretClass",
            ],
        )
    ],
)
def test_get_imports(path, expected_imports):
    parser = PythonParser()

    _imports = parser.get_imports(path)

    assert _imports == expected_imports


@pytest.mark.parametrize(
    "path,expected_classess",
    [
        (
            STUB_PROJECT_1_PATH / "module_1.py",
            [
                ("AbstractClass1", ["ABC"], {}),
                ("AbstractClass2", [], {"metaclass": "ABC"}),
                ("AbstractClass3", [], {"metaclass": "ABC"}),
                ("ConcretClass1", ["AbstractClass1"], {}),
            ],
        )
    ],
)
def test_get_classess(path, expected_classess):
    parser = PythonParser()

    _classes = parser.get_classes(path)

    assert _classes == expected_classess
