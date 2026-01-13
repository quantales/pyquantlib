import pytest

import pyquantlib as ql


@pytest.fixture
def end_criteria():
    """Fixture to create a standard EndCriteria object for testing."""
    return ql.EndCriteria(
        maxIterations=100,
        maxStationaryStateIterations=10,
        rootEpsilon=1e-5,
        functionEpsilon=1e-5,
        gradientNormEpsilon=1e-5
    )


def test_endcriteria_creation_and_properties(end_criteria):
    assert end_criteria.maxIterations == 100
    assert end_criteria.maxStationaryStateIterations == 10
    assert end_criteria.rootEpsilon == 1e-5
    assert end_criteria.functionEpsilon == 1e-5
    assert end_criteria.gradientNormEpsilon == 1e-5


def test_endcriteria_stationary_point(end_criteria):
    # Points far apart - should not end
    has_ended, _ = end_criteria.checkStationaryPoint(
        xOld=1.0, xNew=1.1, statState=0,
        ecType=ql.EndCriteria.Type.Unknown
    )
    assert not has_ended

    # Points close but not enough stationary iterations
    has_ended_close, _ = end_criteria.checkStationaryPoint(
        xOld=1.0, xNew=1.0000001, statState=0,
        ecType=ql.EndCriteria.Type.Unknown
    )
    assert not has_ended_close

    # After exceeding max stationary iterations
    has_ended_final, _ = end_criteria.checkStationaryPoint(
        xOld=1.0, xNew=1.0000001, statState=10,
        ecType=ql.EndCriteria.Type.Unknown
    )
    assert has_ended_final


def test_endcriteria_static_succeeded():
    assert ql.EndCriteria.succeeded(ql.EndCriteria.Type.StationaryPoint)
    assert ql.EndCriteria.succeeded(ql.EndCriteria.Type.StationaryFunctionValue)
    assert ql.EndCriteria.succeeded(ql.EndCriteria.Type.StationaryFunctionAccuracy)
    assert not ql.EndCriteria.succeeded(ql.EndCriteria.Type.None_)
    assert not ql.EndCriteria.succeeded(ql.EndCriteria.Type.ZeroGradientNorm)
    assert not ql.EndCriteria.succeeded(ql.EndCriteria.Type.FunctionEpsilonTooSmall)
    assert not ql.EndCriteria.succeeded(ql.EndCriteria.Type.Unknown)
