import pytest
import numpy as np
import pyquantlib as ql
from pyquantlib.base import Constraint


def test_constraint_abc_exists():
    assert hasattr(ql.base, 'Constraint')


def test_no_constraint():
    c = ql.NoConstraint()
    assert not c.empty()
    assert c.test(ql.Array([1.0, 2.0, 3.0]))
    assert c.test(ql.Array([-1.0, -2.0, -3.0]))


def test_positive_constraint():
    c = ql.PositiveConstraint()
    assert not c.empty()
    assert c.test(ql.Array([1.0, 2.0, 3.0]))
    assert not c.test(ql.Array([-1.0, 2.0, 3.0]))
    assert not c.test(ql.Array([0.0, 1.0, 2.0]))


def test_boundary_constraint():
    c = ql.BoundaryConstraint(0.0, 10.0)
    assert not c.empty()
    assert c.test(ql.Array([1.0, 5.0, 9.0]))
    assert not c.test(ql.Array([-1.0, 5.0, 9.0]))
    assert not c.test(ql.Array([1.0, 5.0, 11.0]))


def test_composite_constraint():
    c1 = ql.PositiveConstraint()
    c2 = ql.BoundaryConstraint(0.0, 10.0)
    c = ql.CompositeConstraint(c1, c2)
    assert not c.empty()
    assert c.test(ql.Array([1.0, 5.0, 9.0]))
    assert not c.test(ql.Array([-1.0, 5.0, 9.0]))
    assert not c.test(ql.Array([1.0, 5.0, 11.0]))
