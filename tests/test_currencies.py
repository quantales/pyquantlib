import pytest

import pyquantlib as ql

# --- Currencies ---

def test_usd_currency():
    usd = ql.USDCurrency()
    assert usd.code() == "USD"
    assert usd.name() == "U.S. dollar"


def test_eur_currency():
    eur = ql.EURCurrency()
    assert eur.code() == "EUR"
    assert eur.name() == "European Euro"


def test_gbp_currency():
    gbp = ql.GBPCurrency()
    assert gbp.code() == "GBP"
    assert gbp.name() == "British pound sterling"


def test_jpy_currency():
    jpy = ql.JPYCurrency()
    assert jpy.code() == "JPY"


def test_currency_inheritance():
    usd = ql.USDCurrency()
    assert isinstance(usd, ql.Currency)


# --- ExchangeRateManager ---

@pytest.fixture(autouse=True)
def clear_exchange_rate_manager():
    """Clear exchange rates before each test."""
    ql.ExchangeRateManager.instance().clear()
    yield
    ql.ExchangeRateManager.instance().clear()


def test_exchangeratemanager_singleton():
    m1 = ql.ExchangeRateManager.instance()
    m2 = ql.ExchangeRateManager.instance()
    assert m1 is m2


def test_exchangeratemanager_add_and_lookup():
    manager = ql.ExchangeRateManager.instance()

    eur = ql.EURCurrency()
    usd = ql.USDCurrency()
    rate = ql.ExchangeRate(eur, usd, 1.1)
    manager.add(rate)

    looked_up = manager.lookup(eur, usd)
    assert looked_up.rate() == pytest.approx(1.1)
    assert looked_up.source() == eur
    assert looked_up.target() == usd
    assert looked_up.type() == ql.ExchangeRate.Type.Direct


def test_exchangeratemanager_triangulation():
    manager = ql.ExchangeRateManager.instance()

    eur = ql.EURCurrency()
    usd = ql.USDCurrency()
    gbp = ql.GBPCurrency()

    manager.add(ql.ExchangeRate(eur, usd, 1.10))
    manager.add(ql.ExchangeRate(usd, gbp, 0.80))

    derived = manager.lookup(eur, gbp)
    assert derived.rate() == pytest.approx(1.10 * 0.80)
    assert derived.type() == ql.ExchangeRate.Type.Derived


def test_exchangeratemanager_no_rate_found():
    manager = ql.ExchangeRateManager.instance()

    eur = ql.EURCurrency()
    gbp = ql.GBPCurrency()

    with pytest.raises(ql.Error, match="no conversion available"):
        manager.lookup(eur, gbp)


def test_exchangeratemanager_clear():
    manager = ql.ExchangeRateManager.instance()

    eur = ql.EURCurrency()
    usd = ql.USDCurrency()
    manager.add(ql.ExchangeRate(eur, usd, 1.1))

    assert manager.lookup(eur, usd).rate() == pytest.approx(1.1)

    manager.clear()

    with pytest.raises(ql.Error, match="no conversion available"):
        manager.lookup(eur, usd)
