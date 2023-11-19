from tests.stubs.stub_project_a.package_a.module_a1 import AbstractClass1A1
from tests.stubs.stub_project_a.package_b import module_b1


class ConcretClass1A1PackageBModuleB2(AbstractClass1A1):
    def abstract_method_1(self):
        module_b1.ConcretClass1A1PackageBModuleB1()
