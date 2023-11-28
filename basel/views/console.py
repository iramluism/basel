from typing import Optional

from basel import config
from basel.reports import Report
from basel.views.formats import ViewFormat
from basel.views.views import View
from tabulate import SEPARATING_LINE
from tabulate import tabulate


class ConsoleView(View):
    _tabulate_formats = {
        ViewFormat.BASIC: "simple",
        ViewFormat.HTML: "html",
    }

    def _get_table_from_report(
        self, report: Report, report_format: ViewFormat = ViewFormat.BASIC
    ):
        data = []
        report_data_len = len(report.data)
        for i, row in enumerate(report.data):
            if not row and (i + 1) != report_data_len:
                data.append(SEPARATING_LINE)
            else:
                data.append(list(row))

        tabulate_format = self._tabulate_formats.get(report_format)
        table = tabulate(data, headers=report.columns, tablefmt=tabulate_format)

        return table

    def render_report(self, report: Report, report_format: Optional[str] = None):
        """Render Report on Console View"""
        if not report_format:
            report_format = ViewFormat.BASIC

        table = self._get_table_from_report(report, report_format)

        if report_format == ViewFormat.HTML:
            return self.html(table)
        else:
            print(table)

    def html(self, table: str):
        with open(config.HTML_REPORT_FILE, "w") as f:
            f.write(table)
