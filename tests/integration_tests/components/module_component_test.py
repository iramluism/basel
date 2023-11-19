from pathlib import Path

from basel.components import ModuleComponentLoader
import pytest

IGONORE_DEPENDENCIES = ["abc"]

STAB_PROJECT_PATH = Path("tests/stubs/stub_project")
STAB_PROJECT_MAIN_DISTANCE = 0.5
STAB_PROJECT_AS_PLANE = {
    "tests.stubs.stub_project": (1, 1, 1),
    "tests.stubs.stub_project.module_1": (1, 0, 0),
    "tests.stubs.stub_project.package_a.module_a2": (0, 0.5, 0.5),
    "tests.stubs.stub_project.package_a.module_a1": (0, 1.0, 0.0),
    "tests.stubs.stub_project.package_a": (1, 1, 1),
}

STAB_PROJECT_A_PATH = Path("tests/stubs/stub_project_a")
STAB_PROJECT_A_MAIN_DISTANCE = 0.59
STAB_PROJECT_A_AS_PLANE = {
    "tests.stubs.stub_project_a": (1, 1, 1),
    "tests.stubs.stub_project_a.module_1": (1, 0, 0),
    "tests.stubs.stub_project_a.package_a.module_a2": (0, 0.5, 0.5),
    "tests.stubs.stub_project_a.package_a.module_a1": (0.33, 1.0, 0.33),
    "tests.stubs.stub_project_a.package_b": (1, 1, 1),
    "tests.stubs.stub_project_a.package_b.module_b1": (0.5, 0, 0.5),
    "tests.stubs.stub_project_a.package_b.module_b2": (1, 0, 0),
    "tests.stubs.stub_project_a.package_b.module_b3": (1, 1, 1),
    "tests.stubs.stub_project_a.package_a": (1, 1, 1),
}


@pytest.mark.parametrize(
    "root_path,expeted_as_plane",
    [
        (STAB_PROJECT_PATH, STAB_PROJECT_AS_PLANE),
        (STAB_PROJECT_A_PATH, STAB_PROJECT_A_AS_PLANE),
    ],
)
def tests_abstraction_stability_plane(root_path, expeted_as_plane):
    loader = ModuleComponentLoader(
        root_path=root_path, ignore_dependencies=IGONORE_DEPENDENCIES
    )

    loader.load_components()

    as_plane = loader.get_as_plane()

    assert as_plane == expeted_as_plane


@pytest.mark.parametrize(
    "root_path,expected_main_distance",
    [
        (STAB_PROJECT_PATH, STAB_PROJECT_MAIN_DISTANCE),
        (STAB_PROJECT_A_PATH, STAB_PROJECT_A_MAIN_DISTANCE),
    ],
)
def tests_calculate_main_distance(root_path: Path, expected_main_distance: float):
    loader = ModuleComponentLoader(
        root_path=root_path, ignore_dependencies=IGONORE_DEPENDENCIES
    )
    loader.load_components()
    main_distance = loader.calculate_main_distance()

    assert main_distance == expected_main_distance
