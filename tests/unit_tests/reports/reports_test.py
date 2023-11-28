from unittest.mock import Mock

from basel.components import Component
from basel.components import Link
from basel.loaders import Loader
from basel.reports import ASReport
from basel.reports import Report
from basel.reports import Reporter
import pytest

MockComponent = Mock(spec=Component)


MOCK_COMPONENTS_LIST = [
    Component(name="Component_A", instability=1, abstraction=1, error=1),
    Component(name="Component_B", instability=0, abstraction=1, error=0),
    Component(name="Component_C", instability=0.25, abstraction=0.5, error=0.25),
    Component(name="Component_D", instability=0.7, abstraction=0, error=0.7),
    Component(name="Component_E", instability=0, abstraction=0, error=1),
]


@pytest.mark.parametrize(
    "components,means,expected_report,filters",
    [
        (
            MOCK_COMPONENTS_LIST,
            (0.39, 0.51, 0.59),
            ASReport(
                columns=["Component", "I", "A", "E"],
                data=[
                    ("Component_A", 1, 1, 1),
                    ("Component_B", 0, 1, 0),
                    ("Component_C", 0.25, 0.5, 0.25),
                    ("Component_D", 0.7, 0, 0.7),
                    ("Component_E", 0, 0, 1),
                    None,
                    ("Mean", 0.39, 0.51, 0.59),
                ],
            ),
            None,
        ),
        (
            MOCK_COMPONENTS_LIST,
            (0.39, 0.51, 0.59),
            ASReport(
                columns=["Component", "I", "A", "E"],
                data=[
                    ("Component_A", 1, 1, 1),
                    None,
                    ("Mean", 0.39, 0.51, 0.59),
                ],
            ),
            {"name": ["match", "Component_A"]},
        ),
        (
            MOCK_COMPONENTS_LIST,
            (0.39, 0.51, 0.59),
            ASReport(
                columns=["Component", "I", "A", "E"],
                data=[
                    ("Component_A", 1, 1, 1),
                    ("Component_B", 0, 1, 0),
                    ("Component_C", 0.25, 0.5, 0.25),
                    ("Component_D", 0.7, 0, 0.7),
                    ("Component_E", 0, 0, 1),
                    None,
                    ("Mean", 0.39, 0.51, 0.59),
                ],
            ),
            {"name": ["match in", ["Component_*", "Component_E"]]},
        ),
        (
            MOCK_COMPONENTS_LIST,
            (0.39, 0.51, 0.59),
            ASReport(
                columns=["Component", "I", "A", "E"],
                data=[
                    ("Component_A", 1, 1, 1),
                    ("Component_B", 0, 1, 0),
                    None,
                    ("Mean", 0.39, 0.51, 0.59),
                ],
            ),
            {"abstraction": 1},
        ),
        (
            MOCK_COMPONENTS_LIST,
            (0.39, 0.51, 0.59),
            ASReport(
                columns=["Component", "I", "A", "E"],
                data=[
                    ("Component_A", 1, 1, 1),
                    ("Component_D", 0.7, 0, 0.7),
                    None,
                    ("Mean", 0.39, 0.51, 0.59),
                ],
            ),
            {"instability": ["gte", 0.7]},
        ),
        (
            MOCK_COMPONENTS_LIST,
            (0.39, 0.51, 0.59),
            ASReport(
                columns=["Component", "I", "A", "E"],
                data=[
                    ("Component_B", 0, 1, 0),
                    ("Component_C", 0.25, 0.5, 0.25),
                    None,
                    ("Mean", 0.39, 0.51, 0.59),
                ],
            ),
            {"error": ["lte", 0.5]},
        ),
        (
            MOCK_COMPONENTS_LIST,
            (0.39, 0.51, 0.59),
            ASReport(
                columns=["Component", "I", "A", "E"],
                data=[
                    ("Component_A", 1, 1, 1),
                    ("Component_C", 0.25, 0.5, 0.25),
                    ("Component_D", 0.7, 0, 0.7),
                    None,
                    ("Mean", 0.39, 0.51, 0.59),
                ],
            ),
            {"instability": ["not eq", 0]},
        ),
        (
            MOCK_COMPONENTS_LIST,
            (0.39, 0.51, 0.59),
            ASReport(
                columns=["Component", "I", "A", "E"],
                data=[
                    ("Component_A", 1, 1, 1),
                    ("Component_D", 0.7, 0, 0.7),
                    ("Component_E", 0, 0, 1),
                    None,
                    ("Mean", 0.39, 0.51, 0.59),
                ],
            ),
            {"error": ["gt", 0.5]},
        ),
    ],
)
def test_get_as_report(components, means, expected_report, filters):
    mock_loader = Mock(spec=Loader)
    mock_loader.get_components.return_value = components
    mock_loader.calculate_mean_instability.return_value = means[0]
    mock_loader.calculate_mean_abstraction.return_value = means[1]
    mock_loader.calculate_mean_error.return_value = means[2]

    reporter = Reporter(mock_loader)

    as_report = reporter.get_as_report(filters)

    assert as_report == expected_report


@pytest.mark.parametrize(
    "components,links,expected_report",
    [
        (
            [
                Component("A"),
                Component("B"),
                Component("C"),
                Component("D"),
            ],
            [
                # A --* B --* C
                # |
                # *
                # D
                Link(source=Component("A"), target=Component("B")),
                Link(source=Component("B"), target=Component("C")),
                Link(source=Component("A"), target=Component("D")),
            ],
            Report(
                columns=["Components", "1", "2", "3", "4"],
                data=[
                    ("1", 0, 0, 0, 0),
                    ("2", 1, 0, 0, 0),
                    ("3", 0, 1, 0, 0),
                    ("4", 1, 0, 0, 0),
                ],
                description="\nLabels:\n1: A\n2: B\n3: C\n4: D\n",
            ),
        )
    ],
)
def test_get_component_links_report(components, links, expected_report):
    mock_loader = Mock(spec=Loader)
    mock_loader.get_components.return_value = components
    mock_loader.get_links.return_value = links

    reporter = Reporter(mock_loader)

    report = reporter.get_component_links_report()

    assert report == expected_report
