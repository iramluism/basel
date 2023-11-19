from collections import namedtuple
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

ASPoint = namedtuple("ASPoint", ["x", "y", "d"])


@dataclass
class Report:
    columns: List[str]
    data: Dict[str, Any]
    footer: Optional[str] = None
