from pathlib import Path
from unittest.mock import Mock

import pytest

from src.client import Basel
from src.components import ModuleComponentLoader
from src.dtos import Report
from src.views import View

IGNORE_DEPENDENCIES = ["abc"]
REPORT_COLUMNS = ["Component", "I", "A", "D"]
STUB_PROJECT_A_PATH = Path("tests/stubs/stub_project_a")
STUB_PROJECT_A_REPORT_DATA = [
    ("tests.stubs.stub_project_a", 1, 1, 1),
    ("tests.stubs.stub_project_a.module_1", 1.0, 0.0, 0.0),
    ("tests.stubs.stub_project_a.package_b.module_b3", 1, 1, 1),
    ("tests.stubs.stub_project_a.package_b.module_b1", 0.5, 0.0, 0.5),
    ("tests.stubs.stub_project_a.package_b", 1, 1, 1),
    ("tests.stubs.stub_project_a.package_b.module_b2", 1.0, 0.0, 0.0),
    ("tests.stubs.stub_project_a.package_a.module_a2", 0.0, 0.5, 0.5),
    ("tests.stubs.stub_project_a.package_a.module_a1", 0.33, 1.0, 0.33),
    ("tests.stubs.stub_project_a.package_a", 1, 1, 1),
]
STUB_PROJECT_A_MEAN_DISTANCE = 0.59

STUB_PROJECT_A_REPORT = Report(
    columns=REPORT_COLUMNS,
    data=STUB_PROJECT_A_REPORT_DATA,
    footer=f"Mean Distance: {STUB_PROJECT_A_MEAN_DISTANCE}",
)


@pytest.mark.parametrize(
    "root_path,ignore_dependencies,expected_report",
    [
        (STUB_PROJECT_A_PATH, IGNORE_DEPENDENCIES, STUB_PROJECT_A_REPORT),
    ],
)
def test_get_report(root_path, ignore_dependencies, expected_report):
    loader = ModuleComponentLoader()
    mock_view = Mock(spec=View)

    cli = Basel(loader=loader, view=mock_view, ignore_depencies=ignore_dependencies)
    report = cli.report(root_path)

    assert report == expected_report
