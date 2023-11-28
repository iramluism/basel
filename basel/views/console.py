from basel.views.views import View


class ConsoleView(View):
    def render_report(self, report: str):
        """Render Report on Console View"""
        print(report)
