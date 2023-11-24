from pathlib import Path
from unittest.mock import Mock

from basel.client import Basel
from basel.loaders import ModuleLoader
from basel.parsers import PythonParser
from basel.reports import ASReport
from basel.reports import Reporter
from basel.views import View
import pytest

IGNORE_DEPENDENCIES = ["abc"]
REPORT_COLUMNS = ["Component", "I", "A", "E"]
STUB_PROJECT_A_PATH = Path("tests/stubs/stub_project_a")

STUB_PROJECT_A_REPORT_DATA = [
    ("tests/stubs/stub_project_a/__init__.py", 1, 1, 1),
    ("tests/stubs/stub_project_a/module_1.py", 1.0, 0.0, 0.0),
    ("tests/stubs/stub_project_a/package_b/__init__.py", 1, 1, 1),
    ("tests/stubs/stub_project_a/package_b/module_b1.py", 0.5, 0.0, 0.5),
    ("tests/stubs/stub_project_a/package_b/module_b2.py", 1.0, 0.0, 0.0),
    ("tests/stubs/stub_project_a/package_b/module_b3.py", 1, 1, 1),
    ("tests/stubs/stub_project_a/package_a/__init__.py", 1, 1, 1),
    ("tests/stubs/stub_project_a/package_a/module_a1.py", 0.25, 1.0, 0.25),
    ("tests/stubs/stub_project_a/package_a/module_a2.py", 0.0, 0.5, 0.5),
]

STUB_PROJECT_A_MEAN_DISTANCE = 0.58

STUB_PROJECT_A_REPORT = ASReport(
    columns=REPORT_COLUMNS,
    data=STUB_PROJECT_A_REPORT_DATA,
)


@pytest.mark.parametrize(
    "root_path,ignore_dependencies,expected_report",
    [
        ([STUB_PROJECT_A_PATH], IGNORE_DEPENDENCIES, STUB_PROJECT_A_REPORT),
    ],
)
def test_get_report(root_path, ignore_dependencies, expected_report):
    parser = PythonParser()
    loader = ModuleLoader(parser)

    reporter = Reporter()
    mock_view = Mock(spec=View)

    cli = Basel(
        loader=loader,
        reporter=reporter,
        view=mock_view,
        ignore_depencies=ignore_dependencies,
    )
    report = cli.report(root_path)

    assert report == expected_report
