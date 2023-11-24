import abc
from abc import ABCMeta
from dataclasses import dataclass  # noqa: F401

from package_a.module_a1 import ConcretClass  # noqa: F401

from .module_2 import *  # noqa


class AbstractClass1(abc.ABC):
    pass


class AbstractClass2(metaclass=abc.ABCMeta):
    pass


class AbstractClass3(metaclass=ABCMeta):
    pass


class ConcretClass1(AbstractClass1):
    pass


obj = ConcretClass()
