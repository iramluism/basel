import abc


class AbstractClass1A2(abc.ABC):
    @abc.abstractmethod
    def abstract_method_1(self):
        raise NotImplementedError()


class ConcretClass1A2(AbstractClass1A2):
    def abstract_method_1(self):
        ...
