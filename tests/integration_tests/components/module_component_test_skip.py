from pathlib import Path

from basel.components import ModuleComponentLoader
import pytest

IGONORE_DEPENDENCIES = ["abc"]

STAB_PROJECT_PATH = Path("tests/stubs/stub_project")
STAB_PROJECT_MAIN_DISTANCE = 0.58
STAB_PROJECT_AS_PLANE = {
    "tests/stubs/stub_project/__init__.py": (1, 1, 1),
    "tests/stubs/stub_project/module_1.py": (1, 0, 0),
    "tests/stubs/stub_project/package_b/module_b1.py": (1, 1, 1),
    "tests/stubs/stub_project/package_a/module_a2.py": (0, 0.5, 0.5),
    "tests/stubs/stub_project/package_a/module_a1.py": (0, 1.0, 0.0),
    "tests/stubs/stub_project/package_a/__init__.py": (1, 1, 1),
}

STAB_PROJECT_A_PATH = Path("tests/stubs/stub_project_a")
STAB_PROJECT_A_MAIN_DISTANCE = 0.58
STAB_PROJECT_A_AS_PLANE = {
    "tests/stubs/stub_project_a/__init__.py": (1, 1, 1),
    "tests/stubs/stub_project_a/module_1.py": (1, 0, 0),
    "tests/stubs/stub_project_a/package_a/module_a2.py": (0, 0.5, 0.5),
    "tests/stubs/stub_project_a/package_a/module_a1.py": (0.25, 1.0, 0.25),
    "tests/stubs/stub_project_a/package_b/__init__.py": (1, 1, 1),
    "tests/stubs/stub_project_a/package_b/module_b2.py": (1, 0, 0),
    "tests/stubs/stub_project_a/package_b/module_b3.py": (1, 1, 1),
    "tests/stubs/stub_project_a/package_b/module_b1.py": (0.5, 0, 0.5),
    "tests/stubs/stub_project_a/package_a/__init__.py": (1, 1, 1),
}

STAB_PROJECT_A_AS_PLANE_FILTER_BY_PACKAGE_B = {
    "tests/stubs/stub_project_a/package_b/__init__.py": (1, 1, 1),
    "tests/stubs/stub_project_a/package_b/module_b2.py": (1, 0, 0),
    "tests/stubs/stub_project_a/package_b/module_b3.py": (1, 1, 1),
    "tests/stubs/stub_project_a/package_b/module_b1.py": (0.5, 0, 0.5),
}


@pytest.mark.skip
@pytest.mark.parametrize(
    "root_path,expeted_as_plane,filter_by_components",
    [
        (STAB_PROJECT_PATH, STAB_PROJECT_AS_PLANE, None),
        (STAB_PROJECT_A_PATH, STAB_PROJECT_A_AS_PLANE, None),
        (
            STAB_PROJECT_A_PATH,
            STAB_PROJECT_A_AS_PLANE_FILTER_BY_PACKAGE_B,
            ["package_b/*"],
        ),
    ],
)
def tests_abstraction_stability_plane(
    root_path, expeted_as_plane, filter_by_components
):
    loader = ModuleComponentLoader(
        root_path=root_path, ignore_dependencies=IGONORE_DEPENDENCIES
    )

    loader.load_components()

    as_plane = loader.get_as_plane(filter_by_components)

    assert as_plane == expeted_as_plane


@pytest.mark.skip
@pytest.mark.parametrize(
    "root_path,ignore_dependencies,expected_mean_distance",
    [
        (STAB_PROJECT_PATH, IGONORE_DEPENDENCIES, STAB_PROJECT_MAIN_DISTANCE),
        (STAB_PROJECT_A_PATH, IGONORE_DEPENDENCIES, STAB_PROJECT_A_MAIN_DISTANCE),
        (
            STAB_PROJECT_A_PATH,
            ["tests/stubs/stub_project_a/package_a/module_a1.py"],
            0.72,
        ),
    ],
)
def tests_calculate_mean_distance(
    root_path: Path, ignore_dependencies, expected_mean_distance: float
):
    loader = ModuleComponentLoader(
        root_path=root_path, ignore_dependencies=ignore_dependencies
    )
    loader.load_components()
    mean_distance = loader.calculate_main_distance()

    assert mean_distance == expected_mean_distance
