from pathlib import Path
from typing import List
from typing import Optional

from basel.loaders import Loader
from basel.reports import Reporter
from basel.views import View


class Basel:
    def __init__(
        self,
        loader: Loader,
        view: View,
        reporter: Reporter,
        ignore_depencies: Optional[List[str]] = None,
    ):
        if not ignore_depencies:
            ignore_depencies = []

        self.reporter = reporter
        self.ignore_dependencies = ignore_depencies
        self.loader = loader
        self.view = view

    def report(
        self,
        root_path: Path,
        ignore_dependencies: Optional[List[str]] = None,
        exclude_components: Optional[List[str]] = None,
        exclude_packages: bool = False,
        filter_by_components: Optional[List[str]] = None,
    ):
        self.loader.load_components(
            paths=root_path,
            ignore_dependencies=ignore_dependencies,
            exclude_components=exclude_components,
            exclude_packages=exclude_packages,
        )

        reporter = self.reporter
        report_filters = {}
        if filter_by_components:
            report_filters["name"] = ["match in", filter_by_components]

        reporter.set_loader(self.loader)
        report = reporter.get_as_report(report_filters)

        self.view.render_report(report)

        return report
