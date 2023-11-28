from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import List
from typing import Optional


class LogType(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


@dataclass
class Log:
    content: str
    type: LogType = LogType.SUCCESS


@dataclass
class Result:
    success: bool = True
    content: Optional[str] = None
    logs: List[Log] = field(default_factory=list)

    def add_log(self, content: str, log_type: Optional[LogType] = None):
        if not log_type:
            log_type = LogType.SUCCESS

        log = Log(content, log_type)
        self.logs.append(log)
