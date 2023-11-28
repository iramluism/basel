from abc import ABC
from dataclasses import dataclass


@dataclass
class Pack:
    name: str
    content: str


class Exporter(ABC):
    def export(self, pack: Pack):
        raise NotImplementedError()


class FileExporter(Exporter):
    def export(self, pack: Pack):
        with open(pack.name, "wb") as f:
            f.write(pack.content)
