from dataclasses import dataclass

from basel.reports.reports import Report


@dataclass
class ASReport(Report):
    name = "AS plane"
    description = "Abstract Stability Report"
