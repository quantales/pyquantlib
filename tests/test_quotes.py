import pytest

import pyquantlib as ql


# Helper observer for testing notifications
class QuoteObserver(ql.base.Observer):
    def __init__(self):
        super().__init__()
        self.update_count = 0

    def update(self):
        self.update_count += 1

    def reset(self):
        self.update_count = 0


# --- SimpleQuote ---

def test_simplequote_construction_default():
    q = ql.SimpleQuote()
    assert not q.isValid()


def test_simplequote_construction_with_value():
    q = ql.SimpleQuote(42.0)
    assert q.isValid()
    assert q.value() == 42.0


def test_simplequote_isinstance_quote():
    q = ql.SimpleQuote(1.0)
    assert isinstance(q, ql.base.Quote)


def test_simplequote_set_value():
    q = ql.SimpleQuote(10.0)
    q.setValue(20.0)
    assert q.value() == 20.0


def test_simplequote_reset():
    q = ql.SimpleQuote(10.0)
    assert q.isValid()
    q.reset()
    assert not q.isValid()


# --- QuoteHandle ---

def test_quotehandle_empty():
    handle = ql.QuoteHandle()
    assert handle.empty()

    with pytest.raises(ql.Error, match="empty Handle cannot be dereferenced"):
        handle.currentLink()


def test_quotehandle_with_quote():
    quote = ql.SimpleQuote(100.0)
    handle = ql.QuoteHandle(quote)

    assert not handle.empty()
    assert handle.currentLink() is quote
    assert handle.get().value() == 100.0


def test_quotehandle_as_observable():
    quote = ql.SimpleQuote(100.0)
    handle = ql.QuoteHandle(quote)
    obs = handle.asObservable()
    assert isinstance(obs, ql.Observable)


def test_quotehandle_notification_propagation():
    quote = ql.SimpleQuote(100.0)
    handle = ql.QuoteHandle(quote)

    observer = QuoteObserver()
    observer.registerWith(handle.asObservable())

    assert observer.update_count == 0

    quote.setValue(150.0)
    assert observer.update_count == 1

    quote.setValue(200.0)
    assert observer.update_count == 2


def test_quotehandle_comparison():
    q1 = ql.SimpleQuote(100.0)
    h1a = ql.QuoteHandle(q1)
    h1b = ql.QuoteHandle(q1)

    q2 = ql.SimpleQuote(200.0)
    h2 = ql.QuoteHandle(q2)

    assert h1a == h1a
    assert h1a != h1b  # Different handles
    assert h1a != h2


def test_quotehandle_register_as_observer_false():
    quote = ql.SimpleQuote(100.0)
    handle = ql.QuoteHandle(quote, registerAsObserver=False)

    observer = QuoteObserver()
    observer.registerWith(handle.asObservable())

    quote.setValue(200.0)
    assert observer.update_count == 0  # Not notified


# --- RelinkableQuoteHandle ---

def test_relinkablequotehandle_empty():
    handle = ql.RelinkableQuoteHandle()
    assert handle.empty()


def test_relinkablequotehandle_initial_quote():
    quote = ql.SimpleQuote(100.0)
    handle = ql.RelinkableQuoteHandle(quote)

    assert not handle.empty()
    assert handle.currentLink() is quote


def test_relinkablequotehandle_link_to():
    handle = ql.RelinkableQuoteHandle()
    assert handle.empty()

    quote = ql.SimpleQuote(123.0)
    handle.linkTo(quote)

    assert not handle.empty()
    assert handle.currentLink() is quote


def test_relinkablequotehandle_relink():
    q1 = ql.SimpleQuote(100.0)
    q2 = ql.SimpleQuote(200.0)

    handle = ql.RelinkableQuoteHandle(q1)
    assert handle.get().value() == 100.0

    handle.linkTo(q2)
    assert handle.get().value() == 200.0
    assert handle.currentLink() is q2


def test_relinkablequotehandle_notification_on_link_to():
    handle = ql.RelinkableQuoteHandle()
    observer = QuoteObserver()
    observer.registerWith(handle.asObservable())

    q1 = ql.SimpleQuote(100.0)
    handle.linkTo(q1)
    assert observer.update_count == 1

    q2 = ql.SimpleQuote(200.0)
    handle.linkTo(q2)
    assert observer.update_count == 2

    # Same quote again - no notification
    handle.linkTo(q2)
    assert observer.update_count == 2


def test_relinkablequotehandle_notification_from_linked_quote():
    handle = ql.RelinkableQuoteHandle()
    observer = QuoteObserver()
    observer.registerWith(handle.asObservable())

    quote = ql.SimpleQuote(100.0)
    handle.linkTo(quote)
    observer.reset()

    quote.setValue(150.0)
    assert observer.update_count == 1


def test_relinkablequotehandle_link_to_register_as_observer_false():
    handle = ql.RelinkableQuoteHandle()
    observer = QuoteObserver()
    observer.registerWith(handle.asObservable())

    quote = ql.SimpleQuote(100.0)
    handle.linkTo(quote, registerAsObserver=False)
    observer.reset()

    quote.setValue(150.0)
    assert observer.update_count == 0  # Not notified


# --- DerivedQuote ---

def test_derivedquote_basic():
    underlying = ql.SimpleQuote(10.0)
    handle = ql.QuoteHandle(underlying)

    derived = ql.DerivedQuote(handle, lambda x: x * 2.0)

    assert derived.isValid()
    assert derived.value() == pytest.approx(20.0)


def test_derivedquote_updates_with_underlying():
    underlying = ql.SimpleQuote(10.0)
    handle = ql.QuoteHandle(underlying)
    derived = ql.DerivedQuote(handle, lambda x: x + 5.0)

    assert derived.value() == pytest.approx(15.0)

    underlying.setValue(20.0)
    assert derived.value() == pytest.approx(25.0)


def test_derivedquote_with_relinkable_handle():
    quote_a = ql.SimpleQuote(10.0)
    quote_b = ql.SimpleQuote(50.0)

    handle = ql.RelinkableQuoteHandle(quote_a)
    derived = ql.DerivedQuote(handle, lambda x: x / 2.0)

    assert derived.value() == pytest.approx(5.0)

    handle.linkTo(quote_b)
    assert derived.value() == pytest.approx(25.0)


def test_derivedquote_error_wrong_return_type():
    underlying = ql.SimpleQuote(10.0)
    handle = ql.QuoteHandle(underlying)
    derived = ql.DerivedQuote(handle, lambda x: "not a number")

    with pytest.raises(TypeError, match="Python function failed to cast result to Real"):
        derived.value()


# --- CompositeQuote ---

def test_compositequote_basic():
    q1 = ql.SimpleQuote(10.0)
    q2 = ql.SimpleQuote(30.0)
    h1 = ql.QuoteHandle(q1)
    h2 = ql.QuoteHandle(q2)

    composite = ql.CompositeQuote(h1, h2, lambda x, y: x + y)

    assert composite.isValid()
    assert composite.value() == pytest.approx(40.0)


def test_compositequote_updates_with_underlying():
    q1 = ql.SimpleQuote(10.0)
    q2 = ql.SimpleQuote(20.0)
    h1 = ql.QuoteHandle(q1)
    h2 = ql.QuoteHandle(q2)

    composite = ql.CompositeQuote(h1, h2, lambda x, y: x * y)

    assert composite.value() == pytest.approx(200.0)

    q1.setValue(5.0)
    assert composite.value() == pytest.approx(100.0)

    q2.setValue(10.0)
    assert composite.value() == pytest.approx(50.0)


def test_compositequote_with_relinkable_handles():
    qa1, qa2 = ql.SimpleQuote(10.0), ql.SimpleQuote(20.0)
    qb1, qb2 = ql.SimpleQuote(100.0), ql.SimpleQuote(200.0)

    h1 = ql.RelinkableQuoteHandle(qa1)
    h2 = ql.RelinkableQuoteHandle(qa2)

    composite = ql.CompositeQuote(h1, h2, lambda x, y: (x + y) / 2.0)

    assert composite.value() == pytest.approx(15.0)

    h1.linkTo(qb1)
    h2.linkTo(qb2)
    assert composite.value() == pytest.approx(150.0)


def test_compositequote_error_wrong_return_type():
    q1 = ql.SimpleQuote(10.0)
    q2 = ql.SimpleQuote(20.0)
    h1 = ql.QuoteHandle(q1)
    h2 = ql.QuoteHandle(q2)

    composite = ql.CompositeQuote(h1, h2, lambda x, y: "not a number")

    with pytest.raises(TypeError, match="Python function failed to cast result to Real"):
        composite.value()


def test_compositequote_error_wrong_arity():
    q1 = ql.SimpleQuote(10.0)
    q2 = ql.SimpleQuote(20.0)
    h1 = ql.QuoteHandle(q1)
    h2 = ql.QuoteHandle(q2)

    # Function with wrong number of arguments
    composite = ql.CompositeQuote(h1, h2, lambda x: x * 2)

    with pytest.raises(TypeError):
        composite.value()
