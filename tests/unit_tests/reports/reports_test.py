from unittest.mock import Mock

from basel.components import Component
from basel.loaders import Loader
from basel.reports import ASReport
from basel.reports import Reporter
import pytest

MockComponent = Mock(spec=Component)


@pytest.mark.parametrize(
    "components,expected_report",
    [
        (
            [
                Component(name="Component_A", instability=1, abstraction=1, error=1),
                Component(name="Component_B", instability=0, abstraction=1, error=0),
                Component(
                    name="Component_C", instability=0.25, abstraction=0.5, error=0.25
                ),
                Component(
                    name="Component_D", instability=0.7, abstraction=0, error=0.7
                ),
                Component(name="Component_E", instability=0, abstraction=0, error=1),
            ],
            ASReport(
                columns=["Component", "I", "A", "E"],
                data=[
                    ("Component_A", 1, 1, 1),
                    ("Component_B", 0, 1, 0),
                    ("Component_C", 0.25, 0.5, 0.25),
                    ("Component_D", 0.7, 0, 0.7),
                    ("Component_E", 0, 0, 1),
                ],
            ),
        )
    ],
)
def test_get_as_report(components, expected_report):
    mock_loader = Mock(spec=Loader)
    mock_loader.get_components.return_value = components

    reporter = Reporter(mock_loader)

    as_report = reporter.get_as_report()

    assert as_report == expected_report
