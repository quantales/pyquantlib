import pytest

import pyquantlib as ql


def test_fixedlocalvolsurface_exists():
    """Verify FixedLocalVolSurface is in main module."""
    assert hasattr(ql, 'FixedLocalVolSurface')


def test_fixedlocalvolsurface_extrapolation_enum():
    """Test extrapolation enum values are accessible."""
    assert hasattr(ql, 'FixedLocalVolExtrapolation')

    const_extrap = ql.FixedLocalVolExtrapolation.ConstantExtrapolation
    interp_extrap = ql.FixedLocalVolExtrapolation.InterpolatorDefaultExtrapolation

    assert const_extrap is not None
    assert interp_extrap is not None
    assert const_extrap != interp_extrap


def test_fixedlocalvolsurface_with_dates():
    """Test FixedLocalVolSurface construction with dates."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    dates = [
        ref_date + ql.Period(1, ql.Months),
        ref_date + ql.Period(3, ql.Months),
        ref_date + ql.Period(6, ql.Months),
        ref_date + ql.Period(1, ql.Years)
    ]

    strikes = [90.0, 100.0, 110.0, 120.0]

    # Matrix: rows = strikes, columns = time points
    local_vol_data = [
        [0.25, 0.24, 0.23, 0.22],  # Strike 90
        [0.23, 0.22, 0.21, 0.20],  # Strike 100
        [0.22, 0.21, 0.20, 0.19],  # Strike 110
        [0.24, 0.23, 0.22, 0.21]   # Strike 120
    ]
    local_vol_matrix = ql.Matrix(local_vol_data)

    flvs = ql.FixedLocalVolSurface(
        ref_date, dates, strikes, local_vol_matrix, dc,
        ql.FixedLocalVolExtrapolation.ConstantExtrapolation,
        ql.FixedLocalVolExtrapolation.ConstantExtrapolation
    )

    assert isinstance(flvs, ql.base.LocalVolTermStructure)
    assert flvs.referenceDate() == ref_date
    assert flvs.maxDate() > ref_date
    assert flvs.minStrike() == pytest.approx(min(strikes))
    assert flvs.maxStrike() == pytest.approx(max(strikes))


def test_fixedlocalvolsurface_with_times():
    """Test FixedLocalVolSurface construction with times."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    times = [0.25, 0.5, 1.0, 2.0]  # years
    strikes = [80.0, 90.0, 100.0, 110.0, 120.0]

    local_vol_data = [
        [0.26, 0.25, 0.24, 0.23],  # Strike 80
        [0.24, 0.23, 0.22, 0.21],  # Strike 90
        [0.23, 0.22, 0.21, 0.20],  # Strike 100
        [0.24, 0.23, 0.22, 0.21],  # Strike 110
        [0.25, 0.24, 0.23, 0.22]   # Strike 120
    ]
    local_vol_matrix = ql.Matrix(local_vol_data)

    flvs = ql.FixedLocalVolSurface(
        ref_date, times, strikes, local_vol_matrix, dc
    )

    assert isinstance(flvs, ql.base.LocalVolTermStructure)

    # Test local vol at grid point
    # times[1] = 0.5, strikes[2] = 100.0 -> matrix[2][1] = 0.22
    assert flvs.localVol(0.5, 100.0) == pytest.approx(0.22)


def test_fixedlocalvolsurface_with_varying_strikes():
    """Test FixedLocalVolSurface with different strikes per time point."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    times = [0.25, 0.5, 1.0]

    # Different strikes for each time point
    strikes_per_time = [
        [90.0, 100.0, 110.0],   # 0.25 years
        [85.0, 95.0, 105.0],   # 0.5 years
        [80.0, 90.0, 100.0]    # 1.0 years
    ]

    local_vol_data = [
        [0.25, 0.26, 0.27],  # Row 0
        [0.23, 0.24, 0.25],  # Row 1
        [0.22, 0.23, 0.24]   # Row 2
    ]
    local_vol_matrix = ql.Matrix(local_vol_data)

    flvs = ql.FixedLocalVolSurface(
        ref_date, times, strikes_per_time, local_vol_matrix, dc,
        ql.FixedLocalVolExtrapolation.InterpolatorDefaultExtrapolation,
        ql.FixedLocalVolExtrapolation.InterpolatorDefaultExtrapolation
    )

    assert isinstance(flvs, ql.base.LocalVolTermStructure)

    # Test at grid point: time=0.5, strike=95.0 -> matrix[1][1] = 0.24
    assert flvs.localVol(0.5, 95.0) == pytest.approx(0.24)


def test_fixedlocalvolsurface_inheritance():
    """Test FixedLocalVolSurface inheritance hierarchy."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    times = [0.5]
    strikes = [100.0, 110.0]
    local_vol_matrix = ql.Matrix([[0.22], [0.21]])

    flvs = ql.FixedLocalVolSurface(
        ref_date, times, strikes, local_vol_matrix, dc
    )

    assert isinstance(flvs, ql.FixedLocalVolSurface)
    assert isinstance(flvs, ql.base.LocalVolTermStructure)
    assert isinstance(flvs, ql.base.VolatilityTermStructure)


def test_fixedlocalvolsurface_in_handle():
    """Test FixedLocalVolSurface works with LocalVolTermStructureHandle."""
    ref_date = ql.Date(15, 6, 2024)
    ql.Settings.instance().evaluationDate = ref_date
    dc = ql.Actual365Fixed()

    times = [0.5, 1.0]
    strikes = [100.0, 110.0]
    local_vol_matrix = ql.Matrix([[0.22, 0.21], [0.21, 0.20]])

    flvs = ql.FixedLocalVolSurface(
        ref_date, times, strikes, local_vol_matrix, dc
    )

    handle = ql.LocalVolTermStructureHandle(flvs)
    assert not handle.empty()

    retrieved = handle.currentLink()
    assert retrieved.localVol(0.5, 100.0) == pytest.approx(0.22)
