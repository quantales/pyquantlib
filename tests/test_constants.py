import pyquantlib as ql


def test_constants_exist():
    assert hasattr(ql, 'MIN_INTEGER')
    assert hasattr(ql, 'MAX_INTEGER')
    assert hasattr(ql, 'MIN_REAL')
    assert hasattr(ql, 'MAX_REAL')
    assert hasattr(ql, 'MIN_POSITIVE_REAL')
    assert hasattr(ql, 'EPSILON')


def test_constants_values():
    assert ql.MIN_INTEGER < 0
    assert ql.MAX_INTEGER > 0
    assert ql.MIN_REAL < 0
    assert ql.MAX_REAL > 0
    assert ql.MIN_POSITIVE_REAL > 0
    assert ql.EPSILON > 0
    assert ql.EPSILON < 1e-10
