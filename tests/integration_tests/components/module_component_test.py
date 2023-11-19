from pathlib import Path

from basel.components import ModuleComponentLoader

STAB_PROJECT_PATH = Path("tests/stubs/stub_project")
STAB_PROJECT_PATH_MAIN_DISTANCE = 0.0
STAB_PROJECT_AS_PLANE = {
    "tests.stubs.stub_project": (1, 1),
    "tests.stubs.stub_project.module_1": (1.0, 0.5),
    "tests.stubs.stub_project.package_a.module_a2": (1.0, 0.5),
    "tests.stubs.stub_project.package_a.module_a1": (1.0, 1.0),
    "tests.stubs.stub_project.package_a": (1, 1),
}


def tests_abstraction_stability_plane():
    loader = ModuleComponentLoader(root_path=STAB_PROJECT_PATH)

    loader.load_components()

    as_plane = loader.get_as_plane()

    assert as_plane == STAB_PROJECT_AS_PLANE


def tests_calculate_main_distance():
    loader = ModuleComponentLoader(root_path=STAB_PROJECT_PATH)

    loader.load_components()

    as_plane = loader.calculate_main_distance()

    assert as_plane == STAB_PROJECT_PATH_MAIN_DISTANCE
