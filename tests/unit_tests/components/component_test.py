from basel.components import Component
from basel.components.classes import ClassNode
from basel.components.modules import ModuleNode
import pytest


@pytest.mark.parametrize(
    "component,expected_classes",
    [
        (
            Component(
                name="Componant_A",
                nodes=[
                    ModuleNode(
                        name="Module_A",
                        children=[
                            ClassNode(
                                name="ClassA",
                            )
                        ],
                    ),
                    ModuleNode(name="Module_B", children=[ClassNode(name="ClassB")]),
                ],
            ),
            [ClassNode(name="ClassA"), ClassNode(name="ClassB")],
        ),
        (
            Component(
                name="Componant_A",
                nodes=[
                    ModuleNode(
                        name="Module_B",
                        children=[
                            ClassNode(
                                name="ClassB", children=[ClassNode(name="MetaClassB")]
                            )
                        ],
                    )
                ],
            ),
            [
                ClassNode(name="ClassB", children=[ClassNode(name="MetaClassB")]),
                ClassNode(name="MetaClassB"),
            ],
        ),
    ],
)
def test_get_classes(component, expected_classes):
    classes = component.get_classes()
    assert expected_classes == classes
