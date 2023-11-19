import abc

from src.dtos import Report
from tabulate import tabulate


class View(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def render_report(self, report: Report):
        raise NotADirectoryError()


class ConsoleView(View):
    def render_report(self, report: Report):
        print(tabulate(report.data, headers=report.columns))
        if report.footer:
            print(report.footer)
