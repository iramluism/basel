import pathlib
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
            "match": lambda a, b: pathlib.Path(a).match(b),
            "match in": lambda a, b: any(pathlib.Path(a).match(r) for r in b),
            "gte": lambda a, b: a >= b,
            "lte": lambda a, b: a <= b,
            "lt": lambda a, b: a < b,
            "gt": lambda a, b: a > b,
        }

        for filter_field, filter_value in filters.items():
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

            conditions[filter_field] = operation(obj_value, filter_value)

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
