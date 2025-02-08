import pytest
import pyquantlib as ql


def test_abstract_termstructure_creates_zombie():
    """
    Verifies that directly instantiating the abstract TermStructure creates
    a non-functional "zombie" object that fails when used.
    """
    # Direct instantiation is possible because we bound the constructor.
    zombie = ql.base.TermStructure(ql.Actual365Fixed())
    assert zombie is not None

    # The zombie object should have an empty calendar and reference date.
    assert zombie.calendar().empty()
    assert zombie.referenceDate() == ql.Date()  # Default date

    # Calling a pure virtual method on the "zombie" object must fail.
    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.maxDate()

# @pytest.mark.skip
def test_python_custom_termstructure_inheritance():
    """
    Tests creating a custom concrete TermStructure in Python to validate
    that its C++ base class is correctly initialized.
    """
    class MyTermStructure(ql.base.TermStructure):
        """A concrete implementation of TermStructure in Python."""
        def __init__(self, reference_date, calendar, day_counter):
            super().__init__(reference_date, calendar, day_counter)

        # --- Implementation of pure virtual methods ---
        def maxDate(self):
            return self.referenceDate() + ql.Period(30, ql.Years)

        def update(self):
            pass

    ref_date = ql.Date(8, 2, 2025)
    calendar = ql.TARGET()
    day_counter = ql.Actual365Fixed()

    my_ts = MyTermStructure(ref_date, calendar, day_counter)

    # 1. Test that the state initialized in the C++ base class is correct.
    assert my_ts.referenceDate() == ref_date
    assert my_ts.dayCounter().name() == day_counter.name()
    assert my_ts.calendar().name() == "TARGET"

    # 2. Test our Python override of the pure virtual method.
    expected_max_date = ref_date + ql.Period(30, ql.Years)
    assert my_ts.maxDate() == expected_max_date

    # 3. Test a C++ method that uses the initialized state.
    target_date = ref_date + ql.Period(1, ql.Years)
    # timeFromReference uses both referenceDate() and dayCounter()
    assert my_ts.timeFromReference(target_date) == pytest.approx(1.0)

