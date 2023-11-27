from basel.reports import Report
from basel.views.views import View
from tabulate import SEPARATING_LINE
from tabulate import tabulate


class ConsoleView(View):
    def render_report(self, report: Report):
        """Render Report on Console View"""

        data = []
        report_data_len = len(report.data)
        for i, row in enumerate(report.data):
            if not row and (i + 1) != report_data_len:
                data.append(SEPARATING_LINE)
            else:
                data.append(list(row))

        table = tabulate(data, headers=report.columns)
        print(table)
