import abc

from tests.stubs.stub_project_a.package_a import module_a2


class AbstractClass1A1(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def abstract_method_1(self):
        raise NotImplementedError()

    def do_something(self):
        module_a2.ConcretClass1A2()
