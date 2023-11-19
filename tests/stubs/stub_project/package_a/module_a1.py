import abc


class AbstractClass1A1(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def abstract_method_1(self):
        raise NotImplementedError()
