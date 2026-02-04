"""
Tests for currencies module.

Corresponds to src/currencies/*.cpp bindings.
"""

import pytest

import pyquantlib as ql


# =============================================================================
# Currency
# =============================================================================


def test_currency_class_exists():
    """Test Currency class is accessible."""
    assert hasattr(ql, 'Currency')


def test_currency_empty():
    """Test default-constructed empty currency."""
    c = ql.Currency()
    assert c.empty()


def test_currency_empty_equality():
    """Test equality of empty currencies."""
    c1 = ql.Currency()
    c2 = ql.Currency()
    assert c1 == c2


# =============================================================================
# Concrete Currencies
# =============================================================================

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
    """Test ExchangeRateManager.clear method."""
    manager = ql.ExchangeRateManager.instance()

    eur = ql.EURCurrency()
    usd = ql.USDCurrency()
    manager.add(ql.ExchangeRate(eur, usd, 1.1))

    assert manager.lookup(eur, usd).rate() == pytest.approx(1.1)

    manager.clear()

    with pytest.raises(ql.Error, match="no conversion available"):
        manager.lookup(eur, usd)


# =============================================================================
# ExchangeRate
# =============================================================================


def test_exchangerate_class_exists():
    """Test ExchangeRate class is accessible."""
    assert hasattr(ql, 'ExchangeRate')


def test_exchangerate_type_enum():
    """Test ExchangeRate.Type enum."""
    assert hasattr(ql.ExchangeRate, 'Direct')
    assert hasattr(ql.ExchangeRate, 'Derived')


def test_exchangerate_chain_method_exists():
    """Test chain static method is accessible."""
    assert hasattr(ql.ExchangeRate, 'chain')


# =============================================================================
# Money
# =============================================================================


@pytest.fixture
def money_env():
    """
    Set up an environment for Money tests.
    Sets up exchange rates, and ensures the
    Money.Settings singleton is reset after each test.
    """
    manager = ql.ExchangeRateManager.instance()
    manager.clear()
    eur = ql.EURCurrency()
    usd = ql.USDCurrency()
    manager.add(ql.ExchangeRate(eur, usd, 1.1))

    money_settings = ql.Money.Settings.instance()
    original_conv_type = money_settings.conversionType
    original_base_ccy = money_settings.baseCurrency

    yield {"eur": eur, "usd": usd}

    manager.clear()
    money_settings.conversionType = original_conv_type
    money_settings.baseCurrency = original_base_ccy


def test_money_creation_and_accessors():
    """Test basic Money creation and accessor methods."""
    eur = ql.EURCurrency()
    m = ql.Money(123.45, eur)

    assert m.value() == 123.45
    assert m.currency() == eur
    assert "123.45 EUR" in str(m)
    assert "<Money: 123.45 EUR>" in repr(m)

    m_empty = ql.Money()
    assert m_empty.value() == 0.0
    assert m_empty.currency().empty()


def test_money_conversion_type_enum():
    """Test Money.ConversionType enum values."""
    assert hasattr(ql.Money, 'NoConversion')
    assert hasattr(ql.Money, 'BaseCurrencyConversion')
    assert hasattr(ql.Money, 'AutomatedConversion')


def test_money_settings_singleton():
    """Test Money.Settings singleton is accessible."""
    settings = ql.Money.Settings.instance()
    assert settings is not None


def test_money_unary_operators():
    """Test Money unary plus and minus operators."""
    eur = ql.EURCurrency()
    m = ql.Money(50.0, eur)

    m_plus = +m
    assert m_plus.value() == 50.0
    assert m_plus.currency() == eur
    assert id(m) != id(m_plus)

    m_minus = -m
    assert m_minus.value() == -50.0
    assert m_minus.currency() == eur


def test_money_inplace_arithmetic():
    """Test Money in-place arithmetic operators."""
    usd = ql.USDCurrency()
    m1 = ql.Money(100.0, usd)
    m2 = ql.Money(25.0, usd)

    m1 += m2
    assert m1.value() == 125.0

    m1 -= m2
    assert m1.value() == 100.0

    m1 *= 2.0
    assert m1.value() == 200.0

    m1 /= 4.0
    assert m1.value() == 50.0


def test_money_comparison_operators():
    """Test Money comparison operators for same-currency objects."""
    gbp = ql.GBPCurrency()
    m100a = ql.Money(100.0, gbp)
    m100b = ql.Money(100.0, gbp)
    m200 = ql.Money(200.0, gbp)

    assert m100a == m100b
    assert m100a != m200
    assert m100a < m200
    assert m200 > m100a
    assert m100a <= m100b
    assert m100a >= m100b


def test_money_rounded_method():
    """Test Money.rounded method."""
    eur = ql.EURCurrency()
    m_unrounded = ql.Money(123.45678, eur)

    m_rounded = m_unrounded.rounded()

    assert m_rounded.value() == pytest.approx(123.46)
    assert m_rounded.currency() == eur
    assert id(m_unrounded) != id(m_rounded)


def test_money_close_functions(money_env):
    """Test close() and close_enough() with NoConversion setting."""
    eur = money_env["eur"]
    usd = money_env["usd"]

    ql.Money.Settings.instance().conversionType = ql.Money.NoConversion

    m1 = ql.Money(100.0, eur)
    m_same = ql.Money(100.0, eur)
    assert ql.close(m1, m_same)

    m_different_currency = ql.Money(100.0, usd)
    with pytest.raises(ql.Error, match="currency mismatch"):
        ql.close(m1, m_different_currency)


def test_money_cross_currency_close_with_conversion(money_env):
    """Test close() across currencies with AutomatedConversion enabled."""
    eur = money_env["eur"]
    usd = money_env["usd"]

    ql.Money.Settings.instance().conversionType = ql.Money.AutomatedConversion
    ql.Money.Settings.instance().baseCurrency = eur

    m_eur = ql.Money(100.0, eur)
    m_usd = ql.Money(110.0, usd)

    assert ql.close(m_eur, m_usd)

    m_usd_different = ql.Money(110.1, usd)
    assert not ql.close(m_eur, m_usd_different)
