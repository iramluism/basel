import pathlib
import re
from typing import Dict
from typing import List
from typing import NewType
from typing import Optional
from typing import Union

from basel import config
from basel.loaders import Loader
from basel.reports.as_plane import ASReport
from basel.reports.formats import ReportFormat
from basel.reports.reports import LinkReport
from basel.reports.reports import Report
from plantuml import PlantUML
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

    def get_component_links_report(
        self, filters: Optional[ReportFilter] = None
    ) -> LinkReport:
        self._loader.load_links()

        out_deps = {}
        for link in self._loader.get_links():
            deps = out_deps.get(link.source.name, [])
            deps.append(link.target.name)
            out_deps[link.source.name] = deps

        data = []

        labels = {}
        for idx, comp in enumerate(self._loader.get_components()):
            if filters and not self._filter(comp, filters):
                continue

            label = str(idx + 1)
            labels[comp.name] = label

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

        footer = "\nLabels:\n"
        for comp_name, label in labels.items():
            footer += f"{label}: {comp_name}\n"

        report = LinkReport(columns=columns, data=data, footer=footer)

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
            ReportFormat.BASIC: (self._format_basic, "*"),
            ReportFormat.HTML: (self._format_html, "*"),
            ReportFormat.MEAN_I: (self._format_instability_mean, [ASReport.name]),
            ReportFormat.MEAN_A: (self._format_abstraction_mean, [ASReport.name]),
            ReportFormat.MEAN_E: (self._format_error_mean, [ASReport.name]),
            ReportFormat.MEAN: (self._format_error_mean, [ASReport.name]),
            ReportFormat.UML: (self._format_uml, [LinkReport.name]),
            ReportFormat.UML_IMG: (self._format_uml_img, [LinkReport.name]),
        }

        if not report_format:
            report_format = ReportFormat.BASIC

        format_fn, available_reports = _report_formats.get(report_format)

        if available_reports != "*" and report.name not in available_reports:
            raise ValueError(
                f"The format {report_format} is not valid for {report.name}"
            )

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

    def _format_uml(self, report: LinkReport) -> str:
        labels = {}
        if not report.footer:
            raise TypeError("Missing Footer")

        for text in report.footer.split("\n"):
            if re.match(r"^\d+:.*$", text):
                idx, comp_name = text.split(": ")
                labels[idx] = comp_name

        source_depx_comp_idx = report.columns[1:]
        uml_staments = []

        for label, component in labels.items():
            uml_staments.append(f"component [{component}]")

        for deps in report.data:
            comp_name = deps[0]
            for idx, dep in enumerate(deps[1:]):
                if not dep:
                    continue

                from_comp_idx = source_depx_comp_idx[idx]
                to_comp_idx = comp_name

                from_comp_name = labels.get(from_comp_idx)
                to_comp_name = labels.get(to_comp_idx)
                uml_staments.append(f"[{from_comp_name}] --> [{to_comp_name}]")

        uml_staments = ["@startuml"] + uml_staments + ["@enduml"]

        uml_text = "\n".join(uml_staments)
        return uml_text

    def _format_uml_img(self, report):
        uml = self._format_uml(report)
        plant_uml = PlantUML(url=config.PLANTUML_URL)
        uml_img = plant_uml.processes(uml)
        return uml_img

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

        if report.footer:
            table += report.footer

        return table
