from typing import Dict
from typing import List
from typing import NewType
from typing import Optional
from typing import Union

from basel.loaders import Loader
from basel.reports.as_plane import ASReport

ReportFilter = NewType("ReportFilter", Dict[str, Union[str, List[str]]])


class Reporter:
    def __init__(self, loader: Optional[Loader] = None):
        self.set_loader(loader)

    def set_loader(self, loader):
        self._loader = loader

    def _filter(self, obj: dict, filters: ReportFilter):
        conditions = dict.fromkeys(filters)
        operations = {
            "eq": lambda a, b: a == b,
            "not eq": lambda a, b: a != b,
        }

        for filter_field, filter_value in filters:
            obj_value = getattr(obj, filter_field, None)

            op = "eq"
            if isinstance(filter_value, list):
                op, filter_value = filter_value

            operation = operations.get(op)
            if not operation:
                raise ValueError(
                    f"Not exists the operator {op},"
                    "posibles value {list(operations.keys())}"
                )

            conditions[filter_value] = operation(filter_value, obj_value)

        match_all_conditions = all(conditions.values())

        return match_all_conditions

    def get_as_report(self, filters: Optional[ReportFilter] = None) -> ASReport:
        data = []
        columns = ["Component", "I", "A", "E"]

        self._loader.calculate_abstraction()
        self._loader.calculate_instability()
        self._loader.calculate_error()

        components = self._loader.get_components()

        for component in components:
            if filters and not self._filter(component, filters):
                continue

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
