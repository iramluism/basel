from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import List
from typing import Optional


@dataclass
class Report:
    name: Optional[str] = None
    columns: List[str] = field(default_factory=list)
    data: List[Any] = field(default_factory=list)
    footer: Optional[str] = None
    description: Optional[str] = None


@dataclass
class LinkReport(Report):
    name: str = "Link Report"
