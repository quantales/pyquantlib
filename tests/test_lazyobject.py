import pytest

from pyquantlib.base import LazyObject

# from pyquantlib import LazyObject


def test_abstract_lazyobject_creates_zombie():
    """
    Documents and verifies that instantiating the abstract LazyObject interface
    succeeds but creates a non-functional "zombie" object.
    """
    # Step 1: Verify that direct instantiation of the abstract interface SUCCEEDS.
    zombie = LazyObject()
    assert zombie is not None, "Instantiation of abstract LazyObject failed."

    # Step 2: Verify that calling a public method that uses the pure virtual
    # implementation FAILS with a RuntimeError.
    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        # We call recalculate(), which internally tries to call the unimplemented
        # performCalculations(), triggering the expected error.
        zombie.recalculate()

    print("\nPASS: Abstract LazyObject correctly created a 'zombie' object.")


def test_python_custom_lazyobject_inheritance():
    """
    Tests creating a custom concrete LazyObject in Python and verifies
    that its overriden methods are called correctly from C++.
    """

    class PyLazyObject(LazyObject):
        """A concrete implementation of LazyObject in Python."""
        def __init__(self):
            super().__init__()
            self.calculation_count = 0

        # --- Implementation of pure virtual methods from the hierarchy ---

        def performCalculations(self):
            """This is the C++-side callback we are testing."""
            self.calculation_count += 1

        def update(self):
            """
            Must be implemented because Observer::update is pure virtual.
            This method would be called by an Observable this object is
            registered with. For this test, it does not need to do anything.
            """
            pass

    # --- Test logic ---

    # 1. Create an instance of our Python subclass
    py_obj = PyLazyObject()
    assert py_obj.calculation_count == 0

    # 2. Test that the public C++ recalculate() method correctly
    #    triggers the Python performCalculations() override.
    py_obj.recalculate()
    assert py_obj.calculation_count == 1, \
        "recalculate() did not trigger the Python performCalculations override."

    # 3. Test that recalculate can be called again.
    py_obj.recalculate()
    assert py_obj.calculation_count == 2, \
        "A second call to recalculate() failed to trigger the override."

    print("\nPASS: Custom Python LazyObject subclass behaved as expected.")
