from basel.loaders import Loader
from basel.reports.as_plane import ASReport


class Reporter:
    def __init__(self, loader: Loader):
        self._loader = loader

    def get_as_report(self) -> ASReport:
        data = []
        columns = ["Component", "I", "A", "E"]
        components = self._loader.get_components()

        for component in components:
            name = component.name
            instability = component.instability
            abstraction = component.abstraction
            error = component.error

            row = (name, instability, abstraction, error)

            data.append(row)

        report = ASReport(
            columns=columns,
            data=data,
        )

        return report
