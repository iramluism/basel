import abc

from basel.dtos import Report
from tabulate import tabulate


class View(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def render_report(self, report: Report):
        raise NotADirectoryError()


class ConsoleView(View):
    def render_report(self, report: Report):
        tabulate(report.data, headers=report.columns)
