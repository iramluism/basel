from unittest.mock import Mock

from basel.components import Component
from basel.components import Link
from basel.loaders import Loader
from basel.reports import ASReport
from basel.reports import LinkReport
from basel.reports import Reporter
from basel.reports import ReportFormat
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
            LinkReport(
                columns=["Components", "1", "2", "3", "4"],
                data=[
                    ("1", 0, 0, 0, 0),
                    ("2", 1, 0, 0, 0),
                    ("3", 0, 1, 0, 0),
                    ("4", 1, 0, 0, 0),
                ],
                footer="\nLabels:\n1: A\n2: B\n3: C\n4: D\n",
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


@pytest.mark.parametrize(
    "report,report_format,expected_result",
    [
        (
            LinkReport(
                columns=["Components", "1", "2", "3", "4"],
                data=[
                    ("1", 0, 0, 0, 0),
                    ("2", 1, 0, 0, 0),
                    ("3", 0, 1, 0, 0),
                    ("4", 1, 0, 0, 0),
                ],
                footer="\nLabels:\n1: A\n2: B\n3: C\n4: D\n",
            ),
            ReportFormat.UML,
            "@startuml\n"
            "component [A]\n"
            "component [B]\n"
            "component [C]\n"
            "component [D]\n"
            "[A] --> [B]\n"
            "[B] --> [C]\n"
            "[A] --> [D]\n"
            "@enduml",
        ),
        (
            LinkReport(
                columns=["Components", "1", "2", "3", "4"],
                data=[
                    ("1", 0, 0, 0, 0),
                    ("2", 1, 0, 0, 0),
                    ("3", 0, 1, 0, 0),
                    ("4", 0, 0, 0, 0),
                ],
                footer="\nLabels:\n1: A\n2: B\n3: C\n4: D\n",
            ),
            ReportFormat.UML,
            "@startuml\n"
            "component [A]\n"
            "component [B]\n"
            "component [C]\n"
            "component [D]\n"
            "[A] --> [B]\n"
            "[B] --> [C]\n"
            "@enduml",
        ),
    ],
)
def test_format_report(report, report_format, expected_result):
    reporter = Reporter()
    result = reporter.format_report(report, report_format)
    assert result == expected_result


@pytest.mark.parametrize(
    "report,report_format",
    [
        (ASReport(), ReportFormat.UML),
        (LinkReport(), ReportFormat.MEAN_I),
        (LinkReport(), ReportFormat.MEAN_A),
        (LinkReport(), ReportFormat.MEAN_E),
    ],
)
def test_raise_error_on_incorrect_report_format(report, report_format):
    reporter = Reporter()
    with pytest.raises(ValueError):
        reporter.format_report(report, report_format)
