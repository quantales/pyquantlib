"""
Tests for copula bindings.

Corresponds to src/math/copulas/*.cpp bindings.
"""

import math

import pytest

import pyquantlib as ql

# Points in the open unit square, away from the boundary singularities
POINTS = [(0.3, 0.6), (0.5, 0.5), (0.8, 0.25), (0.15, 0.9)]


def _phi(x):
    return ql.CumulativeNormalDistribution()(x)


# Closed forms follow the QuantLib implementations. Its Marshall-Olkin copula
# stores 1 - a, giving min(y * x**(1 - a1), x * y**(1 - a2)).
CLOSED_FORMS = [
    ("IndependentCopula", (), lambda x, y: x * y),
    ("MinCopula", (), lambda x, y: max(x + y - 1.0, 0.0)),
    ("MaxCopula", (), lambda x, y: min(x, y)),
    ("ClaytonCopula", (2.0,),
     lambda x, y: max((x ** -2.0 + y ** -2.0 - 1.0) ** (-1.0 / 2.0), 0.0)),
    ("FrankCopula", (3.0,),
     lambda x, y: -1.0 / 3.0 * math.log(
         1.0 + (math.exp(-3.0 * x) - 1.0) * (math.exp(-3.0 * y) - 1.0)
         / (math.exp(-3.0) - 1.0))),
    ("GumbelCopula", (1.5,),
     lambda x, y: math.exp(-((-math.log(x)) ** 1.5 + (-math.log(y)) ** 1.5) ** (1.0 / 1.5))),
    ("AliMikhailHaqCopula", (0.4,),
     lambda x, y: x * y / (1.0 - 0.4 * (1.0 - x) * (1.0 - y))),
    ("FarlieGumbelMorgensternCopula", (0.7,),
     lambda x, y: x * y + 0.7 * x * y * (1.0 - x) * (1.0 - y)),
    ("GalambosCopula", (0.8,),
     lambda x, y: x * y * math.exp(
         ((-math.log(x)) ** -0.8 + (-math.log(y)) ** -0.8) ** (-1.0 / 0.8))),
    ("HuslerReissCopula", (1.2,),
     lambda x, y: x ** _phi(1.0 / 1.2 + 0.6 * math.log(math.log(x) / math.log(y)))
     * y ** _phi(1.0 / 1.2 + 0.6 * math.log(math.log(y) / math.log(x)))),
    ("MarshallOlkinCopula", (0.3, 0.6),
     lambda x, y: min(y * x ** 0.7, x * y ** 0.4)),
    ("PlackettCopula", (2.5),
     lambda x, y: ((1.0 + 1.5 * (x + y))
                   - math.sqrt((1.0 + 1.5 * (x + y)) ** 2 - 4.0 * x * y * 2.5 * 1.5))
     / (2.0 * 1.5)),
]


@pytest.mark.parametrize("name,params,formula", CLOSED_FORMS,
                         ids=[c[0] for c in CLOSED_FORMS])
def test_copula_matches_closed_form(name, params, formula):
    """Each copula reproduces its closed-form expression."""
    params = params if isinstance(params, tuple) else (params,)
    copula = getattr(ql, name)(*params)
    for x, y in POINTS:
        assert copula(x, y) == pytest.approx(formula(x, y), rel=1e-10)


def test_gaussian_copula_matches_bivariate_normal():
    """GaussianCopula evaluates the bivariate normal at the normal quantiles."""
    rho = 0.6
    copula = ql.GaussianCopula(rho)
    bvn = ql.BivariateCumulativeNormalDistribution(rho)
    inv = ql.InverseCumulativeNormal()
    for x, y in POINTS:
        assert copula(x, y) == pytest.approx(bvn(inv(x), inv(y)), rel=1e-10)


@pytest.mark.parametrize("name,params", [
    (c[0], c[1] if isinstance(c[1], tuple) else (c[1],))
    for c in CLOSED_FORMS + [("GaussianCopula", (0.6,), None)]
], ids=[c[0] for c in CLOSED_FORMS] + ["GaussianCopula"])
def test_copula_boundary_conditions(name, params):
    """A copula has uniform margins: C(x, 1) = x and C(1, y) = y."""
    copula = getattr(ql, name)(*params)
    # Evaluated just below 1: Gaussian and Husler-Reiss take logs or quantiles
    # of the argument and are not defined at exactly 1.
    near_one = 1.0 - 1e-9
    for t in (0.2, 0.55, 0.9):
        assert copula(t, near_one) == pytest.approx(t, abs=1e-6)
        assert copula(near_one, t) == pytest.approx(t, abs=1e-6)


@pytest.mark.parametrize("name,params", [
    ("IndependentCopula", ()), ("MinCopula", ()), ("MaxCopula", ()),
    ("ClaytonCopula", (2.0,)), ("GaussianCopula", (0.6,)),
])
def test_copula_rejects_arguments_outside_unit_interval(name, params):
    """Arguments must lie in [0, 1]."""
    copula = getattr(ql, name)(*params)
    with pytest.raises(ql.Error, match="must be in"):
        copula(1.5, 0.5)
    with pytest.raises(ql.Error, match="must be in"):
        copula(0.5, -0.1)


def test_copula_frechet_bounds():
    """Every copula lies between the Min and Max copulas."""
    lower, upper = ql.MinCopula(), ql.MaxCopula()
    for name, params, _ in CLOSED_FORMS:
        params = params if isinstance(params, tuple) else (params,)
        copula = getattr(ql, name)(*params)
        for x, y in POINTS:
            assert lower(x, y) - 1e-12 <= copula(x, y) <= upper(x, y) + 1e-12
