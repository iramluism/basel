import abc
from typing import List


class Parser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_imports(self, path) -> List[str]:
        raise NotADirectoryError()

    @abc.abstractmethod
    def get_classes(self, path) -> List:
        """Parser all classes in the script
        :param path: sript path
        return: List["ClassName", ["Interfaces"], "attributes"]
        """

        raise NotImplementedError()
