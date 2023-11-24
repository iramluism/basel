from basel.reports import Report
from basel.views.views import View
from tabulate import tabulate


class ConsoleView(View):
    def render_report(self, report: Report):
        """Render Report on Console View"""

        print(tabulate(report.data, headers=report.columns))
        if report.footer:
            print(report.footer)
