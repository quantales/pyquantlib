import pytest
import pyquantlib as ql


@pytest.fixture
def vol_surface_data():
    """Setup common test data for BlackVarianceSurface."""
    ref_date = ql.Date(15, 6, 2024)
    calendar = ql.TARGET()
    dc = ql.Actual365Fixed()

    # Dates (maturities)
    dates = [
        ql.Date(15, 9, 2024),   # 3 months
        ql.Date(15, 12, 2024),  # 6 months
        ql.Date(15, 6, 2025),   # 1 year
        ql.Date(15, 6, 2026),   # 2 years
    ]

    # Strikes
    strikes = [80.0, 90.0, 100.0, 110.0, 120.0]

    # Black volatility matrix: rows = strikes, columns = dates
    vol_matrix = ql.Matrix(5, 4)
    vols = [
        [0.25, 0.24, 0.23, 0.22],  # Strike 80.0
        [0.23, 0.22, 0.21, 0.20],  # Strike 90.0
        [0.21, 0.20, 0.19, 0.18],  # Strike 100.0
        [0.23, 0.22, 0.21, 0.20],  # Strike 110.0
        [0.25, 0.24, 0.23, 0.22],  # Strike 120.0
    ]

    for i in range(5):
        for j in range(4):
            vol_matrix[i][j] = vols[i][j]

    return {
        'ref_date': ref_date,
        'calendar': calendar,
        'dc': dc,
        'dates': dates,
        'strikes': strikes,
        'vol_matrix': vol_matrix,
    }


def test_blackvariancesurface_exists():
    """Verify BlackVarianceSurface is in main module."""
    assert hasattr(ql, 'BlackVarianceSurface')


def test_blackvariancesurface_extrapolation_enum():
    """Test extrapolation enum values are accessible."""
    assert hasattr(ql, 'BlackVarianceSurfaceExtrapolation')

    const_extrap = ql.BlackVarianceSurfaceExtrapolation.ConstantExtrapolation
    interp_extrap = ql.BlackVarianceSurfaceExtrapolation.InterpolatorDefaultExtrapolation

    assert const_extrap is not None
    assert interp_extrap is not None
    assert const_extrap != interp_extrap


def test_blackvariancesurface_construction(vol_surface_data):
    """Test basic construction of BlackVarianceSurface."""
    data = vol_surface_data

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc']
    )

    assert surface is not None
    assert surface.referenceDate() == data['ref_date']


def test_blackvariancesurface_construction_with_extrapolation(vol_surface_data):
    """Test construction with explicit extrapolation parameters."""
    data = vol_surface_data

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc'],
        ql.BlackVarianceSurfaceExtrapolation.ConstantExtrapolation,
        ql.BlackVarianceSurfaceExtrapolation.InterpolatorDefaultExtrapolation
    )

    assert surface is not None


def test_blackvariancesurface_inheritance(vol_surface_data):
    """Test BlackVarianceSurface inheritance hierarchy."""
    data = vol_surface_data

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc']
    )

    assert isinstance(surface, ql.BlackVarianceSurface)
    assert isinstance(surface, ql.base.BlackVolTermStructure)
    assert isinstance(surface, ql.base.VolatilityTermStructure)


def test_blackvariancesurface_strike_range(vol_surface_data):
    """Test minStrike() and maxStrike() methods."""
    data = vol_surface_data

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc']
    )

    assert surface.minStrike() == data['strikes'][0]   # 80.0
    assert surface.maxStrike() == data['strikes'][-1]  # 120.0


def test_blackvariancesurface_blackvol_at_grid(vol_surface_data):
    """Test blackVol at grid points."""
    data = vol_surface_data
    ql.Settings.instance().evaluationDate = data['ref_date']

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc']
    )

    # strikes[2] = 100.0, dates[1] = 6M date
    # vol_matrix[2][1] = 0.20
    vol = surface.blackVol(data['dates'][1], data['strikes'][2])
    assert vol == pytest.approx(0.20)


def test_blackvariancesurface_blackvariance(vol_surface_data):
    """Test blackVariance calculation."""
    data = vol_surface_data
    ql.Settings.instance().evaluationDate = data['ref_date']

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc']
    )

    time_to_maturity = data['dc'].yearFraction(data['ref_date'], data['dates'][1])
    variance = surface.blackVariance(time_to_maturity, data['strikes'][2])

    # Variance = vol^2 * time
    expected_variance = 0.20 ** 2 * time_to_maturity
    assert variance == pytest.approx(expected_variance)


def test_blackvariancesurface_set_interpolation(vol_surface_data):
    """Test setInterpolation method."""
    data = vol_surface_data
    ql.Settings.instance().evaluationDate = data['ref_date']

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc']
    )

    off_grid_strike = 95.0

    # Set bicubic interpolation
    surface.setInterpolation("bicubic")
    vol_bicubic = surface.blackVol(data['dates'][1], off_grid_strike)

    # Set bilinear interpolation
    surface.setInterpolation("bilinear")
    vol_bilinear = surface.blackVol(data['dates'][1], off_grid_strike)

    # Both should work, values may differ
    assert vol_bicubic > 0
    assert vol_bilinear > 0

    # At grid point, both should give same result
    vol_at_grid = surface.blackVol(data['dates'][1], data['strikes'][2])
    assert vol_at_grid == pytest.approx(0.20)


def test_blackvariancesurface_in_handle(vol_surface_data):
    """Test BlackVarianceSurface works with BlackVolTermStructureHandle."""
    data = vol_surface_data
    ql.Settings.instance().evaluationDate = data['ref_date']

    surface = ql.BlackVarianceSurface(
        data['ref_date'],
        data['calendar'],
        data['dates'],
        data['strikes'],
        data['vol_matrix'],
        data['dc']
    )

    handle = ql.BlackVolTermStructureHandle(surface)
    assert not handle.empty()

    retrieved = handle.currentLink()
    vol = retrieved.blackVol(data['dates'][1], 100.0)
    assert vol == pytest.approx(0.20)
