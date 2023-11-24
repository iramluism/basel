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
