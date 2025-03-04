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


class TestSimpleQuote:
    def test_construction_default(self):
        q = ql.SimpleQuote()
        assert not q.isValid()

    def test_construction_with_value(self):
        q = ql.SimpleQuote(42.0)
        assert q.isValid()
        assert q.value() == 42.0

    def test_isinstance_quote(self):
        q = ql.SimpleQuote(1.0)
        assert isinstance(q, ql.base.Quote)

    def test_set_value(self):
        q = ql.SimpleQuote(10.0)
        q.setValue(20.0)
        assert q.value() == 20.0

    def test_reset(self):
        q = ql.SimpleQuote(10.0)
        assert q.isValid()
        q.reset()
        assert not q.isValid()


class TestQuoteHandle:
    def test_empty_handle(self):
        handle = ql.QuoteHandle()
        assert handle.empty()

        with pytest.raises(ql.Error, match="empty Handle cannot be dereferenced"):
            handle.currentLink()

    def test_handle_with_quote(self):
        quote = ql.SimpleQuote(100.0)
        handle = ql.QuoteHandle(quote)

        assert not handle.empty()
        assert handle.currentLink() is quote
        assert handle.get().value() == 100.0

    def test_as_observable(self):
        quote = ql.SimpleQuote(100.0)
        handle = ql.QuoteHandle(quote)
        obs = handle.asObservable()
        assert isinstance(obs, ql.Observable)

    def test_notification_propagation(self):
        quote = ql.SimpleQuote(100.0)
        handle = ql.QuoteHandle(quote)

        observer = QuoteObserver()
        observer.registerWith(handle.asObservable())

        assert observer.update_count == 0

        quote.setValue(150.0)
        assert observer.update_count == 1

        quote.setValue(200.0)
        assert observer.update_count == 2

    def test_comparison(self):
        q1 = ql.SimpleQuote(100.0)
        h1a = ql.QuoteHandle(q1)
        h1b = ql.QuoteHandle(q1)

        q2 = ql.SimpleQuote(200.0)
        h2 = ql.QuoteHandle(q2)

        assert h1a == h1a
        assert h1a != h1b  # Different handles
        assert h1a != h2

    def test_register_as_observer_false(self):
        quote = ql.SimpleQuote(100.0)
        handle = ql.QuoteHandle(quote, registerAsObserver=False)

        observer = QuoteObserver()
        observer.registerWith(handle.asObservable())

        quote.setValue(200.0)
        assert observer.update_count == 0  # Not notified


class TestRelinkableQuoteHandle:
    def test_empty_handle(self):
        handle = ql.RelinkableQuoteHandle()
        assert handle.empty()

    def test_initial_quote(self):
        quote = ql.SimpleQuote(100.0)
        handle = ql.RelinkableQuoteHandle(quote)

        assert not handle.empty()
        assert handle.currentLink() is quote

    def test_link_to(self):
        handle = ql.RelinkableQuoteHandle()
        assert handle.empty()

        quote = ql.SimpleQuote(123.0)
        handle.linkTo(quote)

        assert not handle.empty()
        assert handle.currentLink() is quote

    def test_relink(self):
        q1 = ql.SimpleQuote(100.0)
        q2 = ql.SimpleQuote(200.0)

        handle = ql.RelinkableQuoteHandle(q1)
        assert handle.get().value() == 100.0

        handle.linkTo(q2)
        assert handle.get().value() == 200.0
        assert handle.currentLink() is q2

    def test_notification_on_link_to(self):
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

    def test_notification_from_linked_quote(self):
        handle = ql.RelinkableQuoteHandle()
        observer = QuoteObserver()
        observer.registerWith(handle.asObservable())

        quote = ql.SimpleQuote(100.0)
        handle.linkTo(quote)
        observer.reset()

        quote.setValue(150.0)
        assert observer.update_count == 1

    def test_link_to_register_as_observer_false(self):
        handle = ql.RelinkableQuoteHandle()
        observer = QuoteObserver()
        observer.registerWith(handle.asObservable())

        quote = ql.SimpleQuote(100.0)
        handle.linkTo(quote, registerAsObserver=False)
        observer.reset()

        quote.setValue(150.0)
        assert observer.update_count == 0  # Not notified


class TestDerivedQuote:
    def test_basic(self):
        underlying = ql.SimpleQuote(10.0)
        handle = ql.QuoteHandle(underlying)

        derived = ql.DerivedQuote(handle, lambda x: x * 2.0)

        assert derived.isValid()
        assert derived.value() == pytest.approx(20.0)

    def test_updates_with_underlying(self):
        underlying = ql.SimpleQuote(10.0)
        handle = ql.QuoteHandle(underlying)
        derived = ql.DerivedQuote(handle, lambda x: x + 5.0)

        assert derived.value() == pytest.approx(15.0)

        underlying.setValue(20.0)
        assert derived.value() == pytest.approx(25.0)

    def test_with_relinkable_handle(self):
        quote_a = ql.SimpleQuote(10.0)
        quote_b = ql.SimpleQuote(50.0)

        handle = ql.RelinkableQuoteHandle(quote_a)
        derived = ql.DerivedQuote(handle, lambda x: x / 2.0)

        assert derived.value() == pytest.approx(5.0)

        handle.linkTo(quote_b)
        assert derived.value() == pytest.approx(25.0)

    def test_error_wrong_return_type(self):
        underlying = ql.SimpleQuote(10.0)
        handle = ql.QuoteHandle(underlying)
        derived = ql.DerivedQuote(handle, lambda x: "not a number")

        with pytest.raises(TypeError, match="Python function failed to cast result to Real"):
            derived.value()


class TestCompositeQuote:
    def test_basic(self):
        q1 = ql.SimpleQuote(10.0)
        q2 = ql.SimpleQuote(30.0)
        h1 = ql.QuoteHandle(q1)
        h2 = ql.QuoteHandle(q2)

        composite = ql.CompositeQuote(h1, h2, lambda x, y: x + y)

        assert composite.isValid()
        assert composite.value() == pytest.approx(40.0)

    def test_updates_with_underlying(self):
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

    def test_with_relinkable_handles(self):
        qa1, qa2 = ql.SimpleQuote(10.0), ql.SimpleQuote(20.0)
        qb1, qb2 = ql.SimpleQuote(100.0), ql.SimpleQuote(200.0)

        h1 = ql.RelinkableQuoteHandle(qa1)
        h2 = ql.RelinkableQuoteHandle(qa2)

        composite = ql.CompositeQuote(h1, h2, lambda x, y: (x + y) / 2.0)

        assert composite.value() == pytest.approx(15.0)

        h1.linkTo(qb1)
        h2.linkTo(qb2)
        assert composite.value() == pytest.approx(150.0)

    def test_error_wrong_return_type(self):
        q1 = ql.SimpleQuote(10.0)
        q2 = ql.SimpleQuote(20.0)
        h1 = ql.QuoteHandle(q1)
        h2 = ql.QuoteHandle(q2)

        composite = ql.CompositeQuote(h1, h2, lambda x, y: "not a number")

        with pytest.raises(TypeError, match="Python function failed to cast result to Real"):
            composite.value()

    def test_error_wrong_arity(self):
        q1 = ql.SimpleQuote(10.0)
        q2 = ql.SimpleQuote(20.0)
        h1 = ql.QuoteHandle(q1)
        h2 = ql.QuoteHandle(q2)

        # Function with wrong number of arguments
        composite = ql.CompositeQuote(h1, h2, lambda x: x * 2)

        with pytest.raises(TypeError):
            composite.value()
