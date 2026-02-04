"""
Tests for core module.

Corresponds to src/core/*.cpp bindings.
"""

import math

import pytest

import pyquantlib as ql
from pyquantlib.base import Instrument, LazyObject


# =============================================================================
# Settings
# =============================================================================


def test_settings_evaluation_date_get_set():
    """Test Settings evaluation date getter and setter."""
    settings = ql.Settings.instance()

    today = ql.Date.todaysDate()
    custom_date = ql.Date(30, ql.Month.January, 2025)

    settings.evaluationDate = custom_date
    assert settings.evaluationDate == custom_date

    settings.evaluationDate = today
    assert settings.evaluationDate == today


def test_settings_set_evaluation_date_method():
    """Test Settings.setEvaluationDate method."""
    s = ql.Settings.instance()
    today = ql.Date(30, 1, 2025)
    s.setEvaluationDate(today)
    assert s.evaluationDate == today


def test_settings_include_reference_date_events():
    """Test Settings.includeReferenceDateEvents property."""
    settings = ql.Settings.instance()

    settings.includeReferenceDateEvents = True
    assert settings.includeReferenceDateEvents is True

    settings.includeReferenceDateEvents = False
    assert settings.includeReferenceDateEvents is False


def test_settings_include_todays_cash_flows():
    """Test Settings.includeTodaysCashFlows property."""
    settings = ql.Settings.instance()

    settings.includeTodaysCashFlows = True
    assert settings.includeTodaysCashFlows is True

    settings.includeTodaysCashFlows = False
    assert settings.includeTodaysCashFlows is False

    settings.includeTodaysCashFlows = None
    assert settings.includeTodaysCashFlows is None


def test_settings_enforces_todays_historic_fixings():
    """Test Settings.enforcesTodaysHistoricFixings property."""
    settings = ql.Settings.instance()

    settings.enforcesTodaysHistoricFixings = True
    assert settings.enforcesTodaysHistoricFixings is True

    settings.enforcesTodaysHistoricFixings = False
    assert settings.enforcesTodaysHistoricFixings is False


# =============================================================================
# Instrument
# =============================================================================


def test_instrument_abc_exists():
    """Test Instrument ABC exists in base module."""
    assert hasattr(ql.base, 'Instrument')


def test_instrument_abstract_zombie():
    """Test abstract Instrument creates zombie object."""
    zombie = Instrument()

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.isExpired()


def test_instrument_results_class():
    """Test Instrument.results class."""
    results = Instrument.results()
    assert results.value == 0.0


# =============================================================================
# Observable / Observer
# =============================================================================


class PyObserver(ql.base.Observer):
    """A simple Python observer to test callbacks."""
    def __init__(self):
        super().__init__()
        self.notifications_count = 0

    def update(self):
        self.notifications_count += 1

    def reset(self):
        self.notifications_count = 0


def test_observer_registration_and_notification():
    """Test that a Python observer gets notified."""
    observable = ql.Observable()
    observer = PyObserver()

    observer.registerWith(observable)
    assert observer.notifications_count == 0

    observable.notifyObservers()
    assert observer.notifications_count == 1

    observable.notifyObservers()
    assert observer.notifications_count == 2


def test_observer_unregistration():
    """Test observer stops receiving notifications after unregistering."""
    observable = ql.Observable()
    observer = PyObserver()

    observer.registerWith(observable)
    observable.notifyObservers()
    assert observer.notifications_count == 1

    observer.unregisterWith(observable)
    observable.notifyObservers()
    assert observer.notifications_count == 1


def test_observer_multiple_observables_and_unregister_all():
    """Test registration with multiple observables and unregisterWithAll."""
    observable1 = ql.Observable()
    observable2 = ql.Observable()
    observer = PyObserver()

    observer.registerWith(observable1)
    observer.registerWith(observable2)

    observable1.notifyObservers()
    assert observer.notifications_count == 1

    observable2.notifyObservers()
    assert observer.notifications_count == 2

    observer.unregisterWithAll()

    observable1.notifyObservers()
    assert observer.notifications_count == 2

    observable2.notifyObservers()
    assert observer.notifications_count == 2


def test_observer_multiple_observers_on_one_observable():
    """Test multiple observers can register with one observable."""
    observable = ql.Observable()
    observer1 = PyObserver()
    observer2 = PyObserver()

    observer1.registerWith(observable)
    observer2.registerWith(observable)

    observable.notifyObservers()

    assert observer1.notifications_count == 1
    assert observer2.notifications_count == 1

    observer1.unregisterWith(observable)
    observer1.reset()
    observer2.reset()

    observable.notifyObservers()
    assert observer1.notifications_count == 0
    assert observer2.notifications_count == 1


def test_observer_constructor_and_initial_state():
    """Test initial state of PyObserver."""
    observer = PyObserver()
    assert isinstance(observer, ql.base.Observer)
    assert observer.notifications_count == 0


def test_observable_constructor():
    """Test Observable constructor."""
    obs = ql.Observable()
    assert isinstance(obs, ql.Observable)
    obs.notifyObservers()  # Should not raise


# =============================================================================
# LazyObject
# =============================================================================


def test_lazyobject_abstract_creates_zombie():
    """Test abstract LazyObject creates zombie object."""
    zombie = LazyObject()
    assert zombie is not None

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.recalculate()


def test_lazyobject_python_inheritance():
    """Test creating custom LazyObject in Python."""

    class PyLazyObject(LazyObject):
        """A concrete implementation of LazyObject in Python."""
        def __init__(self):
            super().__init__()
            self.calculation_count = 0

        def performCalculations(self):
            self.calculation_count += 1

        def update(self):
            pass

    py_obj = PyLazyObject()
    assert py_obj.calculation_count == 0

    py_obj.recalculate()
    assert py_obj.calculation_count == 1

    py_obj.recalculate()
    assert py_obj.calculation_count == 2


# =============================================================================
# Compounding
# =============================================================================


def test_compounding_values_exist():
    """Test Compounding enum values exist."""
    assert hasattr(ql, 'Simple')
    assert hasattr(ql, 'Compounded')
    assert hasattr(ql, 'Continuous')
    assert hasattr(ql, 'SimpleThenCompounded')
    assert hasattr(ql, 'CompoundedThenSimple')


def test_compounding_enum():
    """Test Compounding enum values match shortcuts."""
    assert ql.Simple == ql.Compounding.Simple
    assert ql.Compounded == ql.Compounding.Compounded
    assert ql.Continuous == ql.Compounding.Continuous


# =============================================================================
# InterestRate
# =============================================================================


@pytest.fixture
def interest_rate_env():
    """Provides common objects for InterestRate tests."""
    day_counter = ql.Actual365Fixed()
    start_date = ql.Date(1, 2, 2025)
    end_date = ql.Date(1, 2, 2026)
    return {
        "rate": 0.05,
        "day_counter": day_counter,
        "compounding": ql.Compounded,
        "frequency": ql.Annual,
        "start_date": start_date,
        "end_date": end_date,
        "time": day_counter.yearFraction(start_date, end_date)
    }


def test_interestrate_constructors(interest_rate_env):
    """Test InterestRate constructors."""
    ir_default = ql.InterestRate()
    assert ir_default.isNull()

    r = interest_rate_env["rate"]
    dc = interest_rate_env["day_counter"]
    comp = interest_rate_env["compounding"]
    freq = interest_rate_env["frequency"]

    ir = ql.InterestRate(r, dc, comp, freq)

    assert ir.rate() == pytest.approx(r)
    assert ir.dayCounter() is not None
    assert ir.compounding() == comp
    assert ir.frequency() == freq


def test_interestrate_inspectors(interest_rate_env):
    """Test InterestRate inspector methods."""
    r = 0.025
    dc = ql.Thirty360(ql.Thirty360.USA)

    ir_discrete = ql.InterestRate(r, dc, ql.Compounded, ql.Quarterly)
    assert ir_discrete.rate() == pytest.approx(r)
    assert ir_discrete.compounding() == ql.Compounded
    assert ir_discrete.frequency() == ql.Quarterly

    ir_continuous = ql.InterestRate(r, dc, ql.Continuous, ql.Quarterly)
    assert ir_continuous.rate() == pytest.approx(r)
    assert ir_continuous.compounding() == ql.Continuous
    assert ir_continuous.frequency() == ql.NoFrequency

    assert ir_discrete.dayCounter().name() == dc.name()
    assert ir_continuous.dayCounter().name() == dc.name()


def test_interestrate_factors(interest_rate_env):
    """Test InterestRate discountFactor and compoundFactor methods."""
    r = interest_rate_env["rate"]
    dc = interest_rate_env["day_counter"]
    start = interest_rate_env["start_date"]
    end = interest_rate_env["end_date"]
    t = interest_rate_env["time"]

    ir_cont = ql.InterestRate(r, dc, ql.Continuous, ql.Annual)

    expected_compound_cont = math.exp(r * t)
    assert ir_cont.compoundFactor(t) == pytest.approx(expected_compound_cont)
    assert ir_cont.discountFactor(t) == pytest.approx(1.0 / expected_compound_cont)

    assert ir_cont.compoundFactor(start, end) == pytest.approx(expected_compound_cont)
    assert ir_cont.discountFactor(start, end) == pytest.approx(1.0 / expected_compound_cont)


def test_interestrate_implied_and_equivalent_rate(interest_rate_env):
    """Test InterestRate impliedRate and equivalentRate methods."""
    r = interest_rate_env["rate"]
    dc = interest_rate_env["day_counter"]
    t = interest_rate_env["time"]

    ir = ql.InterestRate(r, dc, ql.Compounded, ql.Annual)
    compound_factor = ir.compoundFactor(t)

    implied_ir = ql.InterestRate.impliedRate(
        compound_factor, dc, ql.Continuous, ql.Annual, t
    )

    expected_implied_rate = math.log(compound_factor) / t
    assert implied_ir.rate() == pytest.approx(expected_implied_rate)
    assert implied_ir.compounding() == ql.Continuous

    equivalent_ir = ir.equivalentRate(ql.Continuous, ql.Annual, t)

    assert equivalent_ir.rate() == pytest.approx(expected_implied_rate)
    assert equivalent_ir.compounding() == ql.Continuous

    assert implied_ir.rate() == pytest.approx(equivalent_ir.rate())


def test_interestrate_string_representation(interest_rate_env):
    """Test InterestRate string representations."""
    ir = ql.InterestRate(0.03, ql.Actual360(), ql.Compounded, ql.Quarterly)

    s = str(ir)
    assert "3.000000 %" in s
    assert "Actual/360" in s
    assert "Quarterly" in s

    r = repr(ir)
    assert r.startswith("<InterestRate:")
    assert "%" in r
    assert r.endswith(">")


def test_interestrate_float_conversion():
    """Test InterestRate __float__ method."""
    rate_value = 0.045
    ir = ql.InterestRate(rate_value, ql.Actual365Fixed(), ql.Continuous, ql.Annual)

    assert float(ir) == pytest.approx(rate_value)


def test_interestrate_equality():
    """Test InterestRate equality operators."""
    ir1 = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
    ir2 = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
    ir3_diff_rate = ql.InterestRate(0.06, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
    ir4_diff_dc = ql.InterestRate(0.05, ql.Actual360(), ql.Compounded, ql.Annual)
    ir5_diff_comp = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Continuous, ql.Annual)
    ir6_diff_freq = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Semiannual)

    assert ir1 == ir2
    assert not (ir1 == ir3_diff_rate)
    assert not (ir1 == ir4_diff_dc)
    assert not (ir1 == ir5_diff_comp)
    assert not (ir1 == ir6_diff_freq)

    assert not (ir1 != ir2)
    assert ir1 != ir3_diff_rate
    assert ir1 != ir4_diff_dc
    assert ir1 != ir5_diff_comp
    assert ir1 != ir6_diff_freq


def test_interestrate_hashable():
    """Test InterestRate is hashable."""
    ir1 = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
    ir2 = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
    ir3 = ql.InterestRate(0.06, ql.Actual365Fixed(), ql.Compounded, ql.Annual)

    assert hash(ir1) == hash(ir2)
    assert hash(ir1) != hash(ir3)

    rate_set = {ir1, ir2, ir3}
    assert len(rate_set) == 2
    assert ir1 in rate_set
    assert ir2 in rate_set
    assert ir3 in rate_set

    rate_dict = {ir1: "first", ir3: "third"}
    assert rate_dict[ir1] == "first"
    assert rate_dict[ir2] == "first"
