from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from basel.components import ComponentLoader
from basel.dtos import ASPoint
from basel.dtos import Report
from basel.views import View


class Basel:
    def __init__(
        self,
        loader: ComponentLoader,
        view: View,
        ignore_depencies: Optional[List[str]] = None,
    ):
        if not ignore_depencies:
            ignore_depencies = []

        self.ignore_dependencies = ignore_depencies
        self.loader = loader
        self.loader.ignore_deps(self.ignore_dependencies)
        self.view = view

    def _format_report_data(self, data: Dict[str, ASPoint]) -> List[Any]:
        return [(label, point.x, point.y, point.d)
                for label, point in data.items()]

    def report(
        self,
        root_path: Path,
        ignore_dependencies: Optional[List[str]] = None,
        exclude_components: Optional[List[str]] = None,
        exclude_packages: bool = False,
        filter_by_components: Optional[List[str]] = None,
    ):
        self.loader.load_components(
            root_path, ignore_dependencies, exclude_components, exclude_packages
        )

        as_plane = self.loader.get_as_plane(filter_by_components)
        mean_distance = self.loader.calculate_main_distance()
        report = Report(
            columns=["Component", "I", "A", "D"],
            data=self._format_report_data(as_plane),
            footer=f"Mean Distance: {mean_distance}",
        )

        self.view.render_report(report)

        return report
