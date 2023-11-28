import pathlib
from typing import Dict
from typing import List
from typing import NewType
from typing import Optional
from typing import Union

from basel.loaders import Loader
from basel.reports.as_plane import ASReport
from basel.reports.formats import ReportFormat
from basel.reports.reports import Report
from tabulate import SEPARATING_LINE
from tabulate import tabulate

ReportFilter = NewType("ReportFilter", Dict[str, Union[str, List[str]]])


class Reporter:
    def __init__(self, loader: Optional[Loader] = None):
        self.set_loader(loader)

    def set_loader(self, loader):
        self._loader = loader

    def _filter(self, obj: dict, filters: ReportFilter):
        conditions = dict.fromkeys(filters)

        operations = {
            "eq": lambda a, b: a == b,
            "not eq": lambda a, b: a != b,
            "match": lambda a, b: pathlib.Path(a).match(b),
            "match in": lambda a, b: any(pathlib.Path(a).match(r) for r in b),
            "gte": lambda a, b: a >= b,
            "lte": lambda a, b: a <= b,
            "lt": lambda a, b: a < b,
            "gt": lambda a, b: a > b,
        }

        for filter_field, filter_value in filters.items():
            obj_value = getattr(obj, filter_field, None)

            op = "eq"
            if isinstance(filter_value, list):
                op, filter_value = filter_value

            operation = operations.get(op)
            if not operation:
                raise ValueError(
                    f"Not exists the operator {op},"
                    "posibles value {list(operations.keys())}"
                )

            conditions[filter_field] = operation(obj_value, filter_value)

        match_all_conditions = all(conditions.values())

        return match_all_conditions

    def get_component_links_report(self):
        out_deps = {}
        for link in self._loader.get_links():
            deps = out_deps.get(link.source.name, [])
            deps.append(link.target.name)
            out_deps[link.source.name] = deps

        data = []

        labels = {
            comp.name: str(idx + 1)
            for idx, comp in enumerate(self._loader.get_components())
        }
        for eval_comp, idx in labels.items():
            row = [idx]
            for comp in labels.keys():
                value = 0
                deps = out_deps.get(comp, [])
                if eval_comp in deps:
                    value = 1
                row.append(value)

            data.append(tuple(row))

        columns = ["Components"] + list(labels.values())

        description = "\nLabels:\n"
        for comp_name, label in labels.items():
            description += f"{label}: {comp_name}\n"

        report = Report(columns=columns, data=data, description=description)

        return report

    def get_as_report(self, filters: Optional[ReportFilter] = None) -> ASReport:
        data = []
        columns = ["Component", "I", "A", "E"]

        self._loader.calculate_abstraction()
        self._loader.calculate_instability()
        self._loader.calculate_error()

        components = self._loader.get_components()

        for component in components:
            if filters and not self._filter(component, filters):
                continue

            name = component.name
            instability = component.instability
            abstraction = component.abstraction
            error = component.error

            row = (name, instability, abstraction, error)

            data.append(row)

        mean_error = self._loader.calculate_mean_error()
        mean_abstraction = self._loader.calculate_mean_abstraction()
        mean_instability = self._loader.calculate_mean_instability()

        data.append(None)
        data.append(("Mean", mean_instability, mean_abstraction, mean_error))

        report = ASReport(
            columns=columns,
            data=data,
        )

        return report

    def format_report(
        self, report: Report, report_format: Optional[ReportFormat] = None
    ):
        _report_formats = {
            ReportFormat.BASIC: self._format_basic,
            ReportFormat.HTML: self._format_html,
            ReportFormat.MEAN_I: self._format_instability_mean,
            ReportFormat.MEAN_A: self._format_abstraction_mean,
            ReportFormat.MEAN_E: self._format_error_mean,
            ReportFormat.MEAN: self._format_error_mean,
        }

        if not report_format:
            report_format = ReportFormat.BASIC

        format_fn = _report_formats.get(report_format)

        return format_fn(report)

    def _format_basic(self, report: Report) -> str:
        table = self._get_table_from_report(report, report_format=ReportFormat.BASIC)
        return table

    def _format_html(self, report: Report) -> str:
        table = self._get_table_from_report(report, report_format=ReportFormat.HTML)
        return table

    def _format_instability_mean(self, report: Report) -> str:
        totals = report.data[-1]
        i_total = totals[1]
        return i_total

    def _format_abstraction_mean(self, report: Report) -> str:
        totals = report.data[-1]
        i_total = totals[2]
        return i_total

    def _format_error_mean(self, report: Report) -> str:
        totals = report.data[-1]
        i_total = totals[3]
        return i_total

    def _get_table_from_report(
        self, report: Report, report_format: ReportFormat = ReportFormat.BASIC
    ):
        _tabulate_formats = {
            ReportFormat.BASIC: "simple",
            ReportFormat.HTML: "html",
        }

        data = []
        report_data_len = len(report.data)
        for i, row in enumerate(report.data):
            if not row and (i + 1) != report_data_len:
                data.append(SEPARATING_LINE)
            else:
                data.append(list(row))

        tabulate_format = _tabulate_formats.get(report_format, ReportFormat.BASIC)
        table = tabulate(data, headers=report.columns, tablefmt=tabulate_format)

        return table
