import pytest
import pyquantlib as ql
from pyquantlib.base import StochasticProcess, StochasticProcess1D


def test_stochasticprocess_zombie():
    zombie = StochasticProcess()
    with pytest.raises(RuntimeError, match="pure virtual"):
        zombie.size()


def test_stochasticprocess1d_zombie():
    zombie = StochasticProcess1D()
    with pytest.raises(RuntimeError, match="pure virtual"):
        zombie.x0()


def test_stochasticprocess1d_subclass():
    class ConstantProcess(StochasticProcess1D):
        def x0(self): return 100.0
        def drift(self, t, x): return 0.0
        def diffusion(self, t, x): return 0.0
        def evolve(self, t0, x0, dt, dw): return x0

    proc = ConstantProcess()
    assert proc.x0() == 100.0
    assert proc.drift(0.0, 100.0) == 0.0
    assert proc.evolve(0.0, 100.0, 0.01, 0.1) == 100.0


def test_discretization_exists():
    assert hasattr(StochasticProcess1D, 'discretization')
