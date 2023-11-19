from tests.stubs.stub_project.package_a.module_a1 import AbstractClass1A1
from tests.stubs.stub_project.package_a.module_a2 import AbstractClass1A2


class ConcretClass1A1(AbstractClass1A1):
    def abstract_method_1(self):
        # do something
        return


class ConcretClass1A2(AbstractClass1A2):
    def abstract_method_1(self):
        # do something
        return
