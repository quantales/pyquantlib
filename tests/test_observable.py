import pytest
import pyquantlib as ql


class PyObserver(ql.base.Observer):
    """A simple Python observer to test callbacks."""
    def __init__(self):
        super().__init__() # Call the base class constructor
        self.notifications_count = 0

    def update(self): # Matches the signature in PyObserver
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
    assert observer.notifications_count == 1, "Observer's update() method was not called."

    observable.notifyObservers()
    assert observer.notifications_count == 2, "Observer's update() method was not called a second time."
  
def test_observer_unregistration():
    """Test that an observer stops receiving notifications after unregistering."""
    observable = ql.Observable()
    observer = PyObserver()

    observer.registerWith(observable)
    observable.notifyObservers()
    assert observer.notifications_count == 1

    observer.unregisterWith(observable)
    observable.notifyObservers() # This notification should not reach the observer
    assert observer.notifications_count == 1, \
        "Observer was notified after unregistering from the specific observable."
  
def test_observer_multiple_observables_and_unregister_all():
    """Test registration with multiple observables and unregisterWithAll."""
    observable1 = ql.Observable()
    observable2 = ql.Observable()
    observer = PyObserver()

    observer.registerWith(observable1)
    observer.registerWith(observable2)

    observable1.notifyObservers()
    assert observer.notifications_count == 1, "Observer not notified by observable1"

    observable2.notifyObservers()
    assert observer.notifications_count == 2, "Observer not notified by observable2"

    observer.unregisterWithAll()

    observable1.notifyObservers()
    assert observer.notifications_count == 2, \
        "Observer notified by observable1 after unregisterWithAll"

    observable2.notifyObservers()
    assert observer.notifications_count == 2, \
        "Observer notified by observable2 after unregisterWithAll"
  
def test_multiple_observers_on_one_observable():
    """Test that multiple observers can register with one observable."""
    observable = ql.Observable()
    observer1 = PyObserver()
    observer2 = PyObserver()

    observer1.registerWith(observable)
    observer2.registerWith(observable)

    observable.notifyObservers()

    assert observer1.notifications_count == 1, "Observer1 was not notified."
    assert observer2.notifications_count == 1, "Observer2 was not notified."

    # Unregister one, the other should still get updates
    observer1.unregisterWith(observable)
    observer1.reset() # Reset count for observer1
    observer2.reset() # Reset count for observer2

    observable.notifyObservers()
    assert observer1.notifications_count == 0, "Observer1 was notified after unregistering."
    assert observer2.notifications_count == 1, "Observer2 was not notified after observer1 unregistered."
  
def test_observer_constructor_and_initial_state():
    """Test the initial state of the PyObserver."""
    observer = PyObserver()
    assert isinstance(observer, ql.base.Observer)
    assert observer.notifications_count == 0
   
def test_observable_constructor():
    """Test the Observable constructor."""
    obs = ql.Observable()
    assert isinstance(obs, ql.Observable)
    # Attempt to notify with no observers should not error
    try:
        obs.notifyObservers()
    except Exception as e:
        pytest.fail(f"notifyObservers on a new Observable raised an exception: {e}")

