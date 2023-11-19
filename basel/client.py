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
        formatted_data = []

        for label, point in data.items():
            formatted_data.append((label, point.x, point.y, point.d))

        return formatted_data

    def report(self, root_path):
        self.loader.load_components(root_path)

        as_plane = self.loader.get_as_plane()
        mean_distance = self.loader.calculate_main_distance()
        report = Report(
            columns=["Component", "A", "E", "D"],
            data=self._format_report_data(as_plane),
            footer=f"Mean Distance: {mean_distance}",
        )

        self.view.render_report(report)

        return report
