import abc

from basel.reports import Report


class View(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def render_report(self, report: Report):
        raise NotImplementedError()
