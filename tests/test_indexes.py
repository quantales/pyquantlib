"""
Tests for indexes module.

Corresponds to src/indexes/*.cpp bindings.
"""

import pytest

import pyquantlib as ql

# =============================================================================
# Index (ABC)
# =============================================================================


def test_index_abc_exists():
    """Tests that Index ABC is accessible."""
    assert hasattr(ql.base, 'Index')


def test_index_zombie():
    """Tests that direct instantiation creates a zombie object."""
    zombie = ql.base.Index()

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.name()

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.fixingCalendar()


def test_index_python_inheritance():
    """Tests creating a custom Index class in Python."""

    class CustomIndex(ql.base.Index):
        def __init__(self, name, calendar):
            super().__init__()
            self._name = name
            self._calendar = calendar
            self._fixings = {}

        def name(self):
            return self._name

        def fixingCalendar(self):
            return self._calendar

        def isValidFixingDate(self, date):
            return self._calendar.isBusinessDay(date)

        def fixing(self, date, forecastTodaysFixing=False):
            return self._fixings.get(date.serialNumber(), 0.0)

        def update(self):
            pass

    idx = CustomIndex("TEST", ql.TARGET())

    assert idx.name() == "TEST"
    assert idx.fixingCalendar().name() == "TARGET"


# =============================================================================
# InterestRateIndex (ABC)
# =============================================================================


def test_interestrateindex_abc_exists():
    """Test InterestRateIndex ABC is accessible."""
    assert hasattr(ql.base, 'InterestRateIndex')


def test_interestrateindex_zombie():
    """Direct instantiation creates a zombie that fails on pure virtual calls."""
    calendar = ql.TARGET()
    day_counter = ql.Actual360()
    eur = ql.EURCurrency()
    tenor = ql.Period(6, ql.Months)

    zombie = ql.base.InterestRateIndex("DUMMY", tenor, 2, eur, calendar, day_counter)
    assert zombie is not None

    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.maturityDate(ql.Date.todaysDate())


def test_interestrateindex_python_custom():
    """Test Python subclass implementing pure virtual methods."""

    class MyIndex(ql.base.InterestRateIndex):
        def __init__(self, family_name, tenor, fixing_days, currency, calendar, day_counter):
            super().__init__(family_name, tenor, fixing_days, currency, calendar, day_counter)
            self._fixings = {}

        def maturityDate(self, valueDate):
            return self.fixingCalendar().advance(valueDate, self.tenor())

        def forecastFixing(self, fixingDate):
            return 0.05

        def fixing(self, d, forecastTodaysFixing=False):
            if d in self._fixings:
                return self._fixings[d]
            if forecastTodaysFixing:
                return self.forecastFixing(d)
            raise ql.Error(f"Fixing not available for {self.name()} on {d}")

        def update(self):
            pass

        def addFixing(self, d, value):
            self._fixings[d] = value

    calendar = ql.TARGET()
    day_counter = ql.Actual360()
    eur = ql.EURCurrency()
    tenor = ql.Period(6, ql.Months)

    my_index = MyIndex("MyEUR6M", tenor, 2, eur, calendar, day_counter)

    assert my_index.familyName() == "MyEUR6M"
    assert my_index.tenor() == tenor
    assert my_index.currency() == eur
    assert my_index.dayCounter().name() == day_counter.name()


def test_interestrateindex_python_fixing():
    """Test fixing logic in Python subclass."""

    class MyIndex(ql.base.InterestRateIndex):
        def __init__(self, family_name, tenor, fixing_days, currency, calendar, day_counter):
            super().__init__(family_name, tenor, fixing_days, currency, calendar, day_counter)
            self._fixings = {}

        def maturityDate(self, valueDate):
            return self.fixingCalendar().advance(valueDate, self.tenor())

        def forecastFixing(self, fixingDate):
            return 0.05

        def fixing(self, d, forecastTodaysFixing=False):
            if d in self._fixings:
                return self._fixings[d]
            if forecastTodaysFixing:
                return self.forecastFixing(d)
            raise ql.Error("No fixing")

        def update(self):
            pass

        def addFixing(self, d, value):
            self._fixings[d] = value

    calendar = ql.TARGET()
    my_index = MyIndex("TEST", ql.Period(6, ql.Months), 2, ql.EURCurrency(), calendar, ql.Actual360())

    today = ql.Date(14, 6, 2024)
    fixing_date = my_index.fixingDate(today)

    my_index.addFixing(fixing_date, 0.045)
    assert my_index.fixing(fixing_date) == pytest.approx(0.045)

    future_date = calendar.advance(today, 1, ql.Years)
    assert my_index.fixing(future_date, True) == pytest.approx(0.05)


# =============================================================================
# IborIndex
# =============================================================================


@pytest.fixture
def yield_curve():
    """Simple flat yield curve for index tests."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today
    dc = ql.Actual365Fixed()
    return ql.FlatForward(today, 0.05, dc)


def test_iborindex_construction():
    """Test IborIndex construction."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    index = ql.IborIndex(
        "TestIbor",
        ql.Period(3, ql.Months),
        2,  # settlement days
        ql.EURCurrency(),
        ql.TARGET(),
        ql.ModifiedFollowing,
        False,  # end of month
        ql.Actual360(),
    )

    assert index is not None
    assert index.familyName() == "TestIbor"
    assert index.tenor() == ql.Period(3, ql.Months)


def test_iborindex_with_curve(yield_curve):
    """Test IborIndex with forwarding term structure."""
    index = ql.IborIndex(
        "TestIbor",
        ql.Period(6, ql.Months),
        2,
        ql.EURCurrency(),
        ql.TARGET(),
        ql.ModifiedFollowing,
        True,
        ql.Actual360(),
        yield_curve,
    )

    assert index is not None
    assert index.endOfMonth() is True


def test_iborindex_clone(yield_curve):
    """Test IborIndex clone method."""
    index = ql.IborIndex(
        "TestIbor",
        ql.Period(3, ql.Months),
        2,
        ql.EURCurrency(),
        ql.TARGET(),
        ql.ModifiedFollowing,
        False,
        ql.Actual360(),
    )

    cloned = index.clone(ql.YieldTermStructureHandle(yield_curve))
    assert cloned is not None


# =============================================================================
# Euribor
# =============================================================================


def test_euribor_construction():
    """Test Euribor construction with tenor."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    euribor = ql.Euribor(ql.Period(6, ql.Months))

    assert euribor is not None
    assert euribor.tenor() == ql.Period(6, ql.Months)
    assert "Euribor" in euribor.name()


def test_euribor_with_curve(yield_curve):
    """Test Euribor with forwarding term structure."""
    euribor = ql.Euribor(ql.Period(3, ql.Months), yield_curve)

    assert euribor is not None


def test_euribor6m(yield_curve):
    """Test Euribor6M convenience class."""
    euribor = ql.Euribor6M(yield_curve)

    assert euribor is not None
    assert euribor.tenor() == ql.Period(6, ql.Months)


def test_euribor6m_no_curve():
    """Test Euribor6M without forwarding curve."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    euribor = ql.Euribor6M()

    assert euribor is not None
    assert euribor.tenor() == ql.Period(6, ql.Months)


def test_euribor3m(yield_curve):
    """Test Euribor3M convenience class."""
    euribor = ql.Euribor3M(yield_curve)

    assert euribor is not None
    assert euribor.tenor() == ql.Period(3, ql.Months)


def test_euribor1m(yield_curve):
    """Test Euribor1M convenience class."""
    euribor = ql.Euribor1M(yield_curve)

    assert euribor is not None
    assert euribor.tenor() == ql.Period(1, ql.Months)


def test_euribor1y(yield_curve):
    """Test Euribor1Y convenience class."""
    euribor = ql.Euribor1Y(yield_curve)

    assert euribor is not None
    assert euribor.tenor() == ql.Period(1, ql.Years)


def test_euribor_fixing(yield_curve):
    """Test Euribor fixing calculation."""
    today = ql.Date(15, ql.June, 2025)
    ql.Settings.instance().evaluationDate = today

    euribor = ql.Euribor6M(yield_curve)

    # Get a valid fixing date
    fixing_date = euribor.fixingCalendar().advance(
        today, ql.Period(2, ql.Days), ql.Following
    )

    # Should be able to forecast fixing
    if euribor.isValidFixingDate(fixing_date):
        rate = euribor.fixing(fixing_date, True)
        assert rate == pytest.approx(0.04993839342800618, rel=1e-5)


# =============================================================================
# OvernightIndex (RFR): SOFR, ESTR, SONIA
# =============================================================================


@pytest.fixture(scope="module")
def flat_curve():
    """Flat yield curve for RFR index tests."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.evaluationDate = today
    curve = ql.FlatForward(today, 0.035, ql.Actual365Fixed())
    return {"today": today, "curve": curve}


def test_sofr_construction():
    """Test Sofr construction without curve."""
    sofr = ql.Sofr()
    assert sofr is not None
    assert "SOFR" in sofr.name()


def test_sofr_with_curve(flat_curve):
    """Test Sofr construction with forwarding curve."""
    sofr = ql.Sofr(flat_curve["curve"])
    assert sofr is not None
    assert "SOFR" in sofr.name()


def test_sofr_properties():
    """Test Sofr index properties."""
    sofr = ql.Sofr()
    assert sofr.fixingDays() == 0
    assert sofr.dayCounter() == ql.Actual360()


def test_estr_construction():
    """Test Estr construction without curve."""
    estr = ql.Estr()
    assert estr is not None
    assert "ESTR" in estr.name()


def test_estr_with_curve(flat_curve):
    """Test Estr construction with forwarding curve."""
    estr = ql.Estr(flat_curve["curve"])
    assert estr is not None


def test_estr_properties():
    """Test Estr index properties."""
    estr = ql.Estr()
    assert estr.fixingDays() == 0
    assert estr.dayCounter() == ql.Actual360()


def test_sonia_construction():
    """Test Sonia construction without curve."""
    sonia = ql.Sonia()
    assert sonia is not None
    assert "Sonia" in sonia.name()


def test_sonia_with_curve(flat_curve):
    """Test Sonia construction with forwarding curve."""
    sonia = ql.Sonia(flat_curve["curve"])
    assert sonia is not None


def test_sonia_properties():
    """Test Sonia index properties."""
    sonia = ql.Sonia()
    assert sonia.fixingDays() == 0
    assert sonia.dayCounter() == ql.Actual365Fixed()


# =============================================================================
# SwapIndex
# =============================================================================


def test_swapindex_construction(flat_curve):
    """Test SwapIndex construction."""
    euribor6m = ql.Euribor(ql.Period(6, ql.Months), flat_curve["curve"])
    swap_index = ql.SwapIndex(
        "EurSwap", ql.Period(5, ql.Years), 2,
        ql.EURCurrency(), ql.TARGET(),
        ql.Period(1, ql.Years), ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        euribor6m,
    )
    assert swap_index is not None
    assert swap_index.fixedLegConvention() == ql.Unadjusted


def test_swapindex_with_discount(flat_curve):
    """Test SwapIndex construction with discounting curve."""
    euribor6m = ql.Euribor(ql.Period(6, ql.Months), flat_curve["curve"])
    swap_index = ql.SwapIndex(
        "EurSwap", ql.Period(5, ql.Years), 2,
        ql.EURCurrency(), ql.TARGET(),
        ql.Period(1, ql.Years), ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        euribor6m, flat_curve["curve"],
    )
    assert swap_index is not None
    assert swap_index.exogenousDiscount()


def test_swapindex_properties(flat_curve):
    """Test SwapIndex property accessors."""
    euribor6m = ql.Euribor(ql.Period(6, ql.Months), flat_curve["curve"])
    swap_index = ql.SwapIndex(
        "EurSwap", ql.Period(5, ql.Years), 2,
        ql.EURCurrency(), ql.TARGET(),
        ql.Period(1, ql.Years), ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        euribor6m,
    )
    assert swap_index.fixedLegTenor() == ql.Period(1, ql.Years)
    assert swap_index.iborIndex() is not None
    assert not swap_index.exogenousDiscount()


# =============================================================================
# OvernightIndexedSwapIndex
# =============================================================================


def test_overnightindexedswapindex_construction(flat_curve):
    """Test OvernightIndexedSwapIndex construction."""
    estr = ql.Estr(flat_curve["curve"])
    ois_index = ql.OvernightIndexedSwapIndex(
        "EstrSwap", ql.Period(1, ql.Years), 2,
        ql.EURCurrency(), estr,
    )
    assert ois_index is not None


def test_overnightindexedswapindex_with_averaging(flat_curve):
    """Test OvernightIndexedSwapIndex with explicit averaging."""
    sofr = ql.Sofr(flat_curve["curve"])
    ois_index = ql.OvernightIndexedSwapIndex(
        "SofrSwap", ql.Period(2, ql.Years), 2,
        ql.USDCurrency(), sofr,
        telescopicValueDates=True,
        averagingMethod=ql.RateAveraging.Type.Simple,
    )
    assert ois_index is not None


# =============================================================================
# Concrete SwapIndex subclasses (src/indexes/swap/)
# =============================================================================

SWAP_INDEX_CLASSES = [
    "EuriborSwapIsdaFixA",
    "EuriborSwapIsdaFixB",
    "EuriborSwapIfrFix",
    "EurLiborSwapIsdaFixA",
    "EurLiborSwapIsdaFixB",
    "EurLiborSwapIfrFix",
    "UsdLiborSwapIsdaFixAm",
    "UsdLiborSwapIsdaFixPm",
    "JpyLiborSwapIsdaFixAm",
    "JpyLiborSwapIsdaFixPm",
    "GbpLiborSwapIsdaFix",
    "ChfLiborSwapIsdaFix",
]


@pytest.mark.parametrize("cls_name", SWAP_INDEX_CLASSES)
def test_swapindex_subclass_tenor_only(cls_name):
    """Test constructing swap index subclasses with tenor only."""
    today = ql.Date(15, ql.January, 2025)
    ql.Settings.instance().evaluationDate = today
    cls = getattr(ql, cls_name)
    idx = cls(ql.Period("10Y"))
    assert isinstance(idx, ql.SwapIndex)
    assert idx.tenor() == ql.Period("10Y")


@pytest.mark.parametrize("cls_name", SWAP_INDEX_CLASSES)
def test_swapindex_subclass_with_curve(cls_name, flat_curve):
    """Test constructing swap index subclasses with forwarding curve."""
    cls = getattr(ql, cls_name)
    idx = cls(ql.Period("5Y"), flat_curve["curve"])
    assert isinstance(idx, ql.SwapIndex)
    assert idx.tenor() == ql.Period("5Y")


@pytest.mark.parametrize("cls_name", SWAP_INDEX_CLASSES)
def test_swapindex_subclass_with_two_curves(cls_name, flat_curve):
    """Test constructing swap index subclasses with forwarding and discounting."""
    cls = getattr(ql, cls_name)
    curve = flat_curve["curve"]
    idx = cls(ql.Period("2Y"), curve, curve)
    assert isinstance(idx, ql.SwapIndex)
    assert idx.exogenousDiscount()


@pytest.mark.parametrize("cls_name", SWAP_INDEX_CLASSES)
def test_swapindex_subclass_with_handle(cls_name, flat_curve):
    """Test constructing swap index subclasses with explicit handle."""
    cls = getattr(ql, cls_name)
    handle = ql.YieldTermStructureHandle(flat_curve["curve"])
    idx = cls(ql.Period("10Y"), handle)
    assert isinstance(idx, ql.SwapIndex)


# =============================================================================
# Region
# =============================================================================


def test_region_concrete_construction():
    """Test constructing concrete regions."""
    us = ql.USRegion()
    assert us.name() == "USA"
    assert us.code() == "US"

    uk = ql.UKRegion()
    assert uk.name() == "UK"
    assert uk.code() == "UK"

    eu = ql.EURegion()
    assert eu.name() == "EU"
    assert eu.code() == "EU"


def test_region_all_concrete():
    """Test all concrete region classes exist and construct."""
    regions = {
        "AustraliaRegion": ("Australia", "AU"),
        "EURegion": ("EU", "EU"),
        "FranceRegion": ("France", "FR"),
        "UKRegion": ("UK", "UK"),
        "USRegion": ("USA", "US"),
        "ZARegion": ("South Africa", "ZA"),
    }
    for cls_name, (expected_name, expected_code) in regions.items():
        cls = getattr(ql, cls_name)
        r = cls()
        assert r.name() == expected_name
        assert r.code() == expected_code


def test_custom_region():
    """Test CustomRegion construction."""
    r = ql.CustomRegion("Testland", "TL")
    assert r.name() == "Testland"
    assert r.code() == "TL"


def test_region_equality():
    """Test Region equality operators."""
    us1 = ql.USRegion()
    us2 = ql.USRegion()
    uk = ql.UKRegion()
    assert us1 == us2
    assert us1 != uk


def test_region_str():
    """Test Region string representation."""
    us = ql.USRegion()
    assert str(us) == "USA"


# =============================================================================
# InflationIndex (ABC)
# =============================================================================


def test_inflationindex_abc_exists():
    """Test that InflationIndex ABC is accessible."""
    assert hasattr(ql.base, "InflationIndex")


def test_inflationindex_zombie():
    """Test that direct instantiation creates a zombie object."""
    zombie = ql.base.InflationIndex(
        "TEST", ql.USRegion(), False, ql.Monthly,
        ql.Period(1, ql.Months), ql.USDCurrency()
    )
    with pytest.raises(RuntimeError, match="Tried to call pure virtual function"):
        zombie.fixing(ql.Date(15, ql.January, 2025))


# =============================================================================
# CPI
# =============================================================================


def test_cpi_enum():
    """Test CPI InterpolationType enum values."""
    assert hasattr(ql.CPI, "AsIndex")
    assert hasattr(ql.CPI, "Flat")
    assert hasattr(ql.CPI, "Linear")
    # Values are accessible directly
    assert ql.CPI.AsIndex != ql.CPI.Flat
    assert ql.CPI.Flat != ql.CPI.Linear


# =============================================================================
# ZeroInflationIndex
# =============================================================================


def test_zeroinflationindex_construction():
    """Test ZeroInflationIndex construction without term structure."""
    idx = ql.ZeroInflationIndex(
        "CPI", ql.USRegion(), False, ql.Monthly,
        ql.Period(1, ql.Months), ql.USDCurrency()
    )
    assert idx.familyName() == "CPI"
    assert idx.region() == ql.USRegion()
    assert idx.revised() is False
    assert idx.frequency() == ql.Monthly
    assert idx.availabilityLag() == ql.Period(1, ql.Months)
    assert isinstance(idx, ql.base.InflationIndex)


def test_zeroinflationindex_fixings():
    """Test adding and retrieving fixings on a ZeroInflationIndex."""
    idx = ql.ZeroInflationIndex(
        "CPI", ql.USRegion(), False, ql.Monthly,
        ql.Period(1, ql.Months), ql.USDCurrency()
    )
    # Add a fixing
    fixing_date = ql.Date(1, ql.January, 2024)
    idx.addFixing(fixing_date, 308.417)
    assert idx.fixing(fixing_date) == pytest.approx(308.417)


# =============================================================================
# YoYInflationIndex
# =============================================================================


def test_yoyinflationindex_from_zero():
    """Test YoYInflationIndex constructed as a ratio of a zero index."""
    zero_idx = ql.ZeroInflationIndex(
        "CPI", ql.USRegion(), False, ql.Monthly,
        ql.Period(1, ql.Months), ql.USDCurrency()
    )
    yoy_idx = ql.YoYInflationIndex(zero_idx)
    assert yoy_idx.ratio() is True
    assert yoy_idx.underlyingIndex() is not None
    assert isinstance(yoy_idx, ql.base.InflationIndex)


def test_yoyinflationindex_quoted():
    """Test standalone quoted YoYInflationIndex construction."""
    yoy_idx = ql.YoYInflationIndex(
        "YY_CPI", ql.USRegion(), False, ql.Monthly,
        ql.Period(1, ql.Months), ql.USDCurrency()
    )
    assert yoy_idx.familyName() == "YY_CPI"
    assert yoy_idx.ratio() is False


# =============================================================================
# Concrete Inflation Indexes
# =============================================================================


ZERO_INFLATION_INDEXES = ["USCPI", "UKRPI", "EUHICP", "EUHICPXT"]
YOY_INFLATION_INDEXES = ["YYUSCPI", "YYUKRPI", "YYEUHICP", "YYEUHICPXT"]


@pytest.mark.parametrize("cls_name", ZERO_INFLATION_INDEXES)
def test_zero_inflation_index_construction(cls_name):
    """Test constructing concrete zero inflation indexes."""
    cls = getattr(ql, cls_name)
    idx = cls()
    assert isinstance(idx, ql.ZeroInflationIndex)
    assert isinstance(idx, ql.base.InflationIndex)
    assert idx.frequency() == ql.Monthly


@pytest.mark.parametrize("cls_name", YOY_INFLATION_INDEXES)
def test_yoy_inflation_index_construction(cls_name):
    """Test constructing concrete YoY inflation indexes."""
    cls = getattr(ql, cls_name)
    idx = cls()
    assert isinstance(idx, ql.YoYInflationIndex)
    assert isinstance(idx, ql.base.InflationIndex)
    assert idx.frequency() == ql.Monthly


def test_uscpi_properties():
    """Test USCPI index properties."""
    idx = ql.USCPI()
    assert idx.familyName() == "CPI"
    assert idx.region() == ql.USRegion()
    assert idx.currency() == ql.USDCurrency()
    assert idx.availabilityLag() == ql.Period(1, ql.Months)


def test_ukrpi_properties():
    """Test UKRPI index properties."""
    idx = ql.UKRPI()
    assert idx.familyName() == "RPI"
    assert idx.region() == ql.UKRegion()
    assert idx.currency() == ql.GBPCurrency()


def test_euhicp_properties():
    """Test EUHICP index properties."""
    idx = ql.EUHICP()
    assert idx.familyName() == "HICP"
    assert idx.region() == ql.EURegion()
    assert idx.currency() == ql.EURCurrency()


def test_uscpi_fixings():
    """Test adding fixings to USCPI."""
    idx = ql.USCPI()
    date1 = ql.Date(1, ql.January, 2024)
    date2 = ql.Date(1, ql.February, 2024)
    idx.addFixing(date1, 308.417)
    idx.addFixing(date2, 310.326)
    assert idx.fixing(date1) == pytest.approx(308.417)
    assert idx.fixing(date2) == pytest.approx(310.326)
    idx.clearFixings()


# =============================================================================
# AUCPI / YYAUCPI (Australian CPI)
# =============================================================================


def test_aucpi_construction():
    """Test AUCPI construction with frequency and revised."""
    idx = ql.AUCPI(ql.Quarterly, False)
    assert isinstance(idx, ql.ZeroInflationIndex)
    assert idx.frequency() == ql.Quarterly


def test_aucpi_revised():
    """Test AUCPI with revised flag."""
    idx = ql.AUCPI(ql.Quarterly, True)
    assert idx is not None
    assert idx.revised() is True


def test_aucpi_properties():
    """Test AUCPI index properties."""
    idx = ql.AUCPI(ql.Quarterly, False)
    assert idx.region() == ql.AustraliaRegion()
    assert idx.currency() == ql.AUDCurrency()


def test_yyaucpi_construction():
    """Test YYAUCPI construction with frequency and revised."""
    idx = ql.YYAUCPI(ql.Quarterly, False)
    assert isinstance(idx, ql.YoYInflationIndex)
    assert idx.frequency() == ql.Quarterly


def test_yyaucpi_revised():
    """Test YYAUCPI with revised flag."""
    idx = ql.YYAUCPI(ql.Quarterly, True)
    assert idx is not None
    assert idx.revised() is True


# =============================================================================
# FRHICP / YYFRHICP (French HICP)
# =============================================================================


def test_frhicp_construction():
    """Test FRHICP construction."""
    idx = ql.FRHICP()
    assert isinstance(idx, ql.ZeroInflationIndex)
    assert idx.frequency() == ql.Monthly


def test_frhicp_properties():
    """Test FRHICP index properties."""
    idx = ql.FRHICP()
    assert idx.region() == ql.FranceRegion()
    assert idx.currency() == ql.EURCurrency()


def test_yyfrhicp_construction():
    """Test YYFRHICP construction."""
    idx = ql.YYFRHICP()
    assert isinstance(idx, ql.YoYInflationIndex)
    assert idx.frequency() == ql.Monthly


# =============================================================================
# ZACPI / YYZACPI (South African CPI)
# =============================================================================


def test_zacpi_construction():
    """Test ZACPI construction."""
    idx = ql.ZACPI()
    assert isinstance(idx, ql.ZeroInflationIndex)
    assert idx.frequency() == ql.Monthly


def test_zacpi_properties():
    """Test ZACPI index properties."""
    idx = ql.ZACPI()
    assert idx.region() == ql.ZARegion()
    assert idx.currency() == ql.ZARCurrency()


def test_yyzacpi_construction():
    """Test YYZACPI construction."""
    idx = ql.YYZACPI()
    assert isinstance(idx, ql.YoYInflationIndex)
    assert idx.frequency() == ql.Monthly
