from basel import utils
import pytest


@pytest.mark.parametrize(
    "in_deps,out_deps,expected_instability",
    [(0, 0, 1), (1, 1, 0.5), (1, 2, 0.67), (3, 1, 0.25), (0, 1, 1)],
)
def test_instability(in_deps, out_deps, expected_instability):
    instability = utils.instability(in_deps, out_deps)
    assert instability == expected_instability


@pytest.mark.parametrize(
    "in_deps,out_deps,expected_stability",
    [(0, 0, 0), (1, 1, 0.5), (1, 2, 0.33), (3, 1, 0.75), (0, 1, 0)],
)
def test_stability(in_deps, out_deps, expected_stability):
    stability = utils.stability(in_deps, out_deps)
    assert stability == expected_stability


@pytest.mark.parametrize(
    "in_deps,out_deps,expected_abstraction",
    [(0, 0, 1), (1, 1, 0.5), (1, 2, 0.33), (3, 1, 0.75), (0, 1, 0)],
)
def test_abstraction(in_deps, out_deps, expected_abstraction):
    abstraction = utils.abstraction(in_deps, out_deps)
    assert abstraction == expected_abstraction


@pytest.mark.parametrize(
    "in_deps,out_deps,expected_implementation",
    [(0, 0, 0), (1, 1, 0.5), (1, 2, 0.67), (3, 1, 0.25), (0, 1, 1)],
)
def test_implementation(in_deps, out_deps, expected_implementation):
    implementation = utils.implementation(in_deps, out_deps)
    assert implementation == expected_implementation


@pytest.mark.parametrize(
    "instability,abstraction,expected_error",
    [(1, 1, 1), (1, 0, 0), (0.3, 0.8, 0.1), (0, 0, 1), (0.8, 0.8, 0.6)],
)
def test_abs_error_to_main_sequence(instability, abstraction, expected_error):
    error = utils.abs_error_to_main_sequence(instability, abstraction)
    assert error == expected_error


@pytest.mark.parametrize(
    "values,expected_mean", [([1, 0, 0, 0], 0.25), ([], 0), ([2, 2, 3, 4], 2.75)]
)
def test_mean(values, expected_mean):
    _mean = utils.mean(values)
    assert _mean == expected_mean
