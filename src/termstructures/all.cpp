/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include "pyquantlib/binding_manager.h"

DECLARE_MODULE_BINDINGS(termstructures_bindings) {
    // Abstract base classes
    ADD_BASE_BINDING(ql_termstructures::yieldtermstructure,
        "YieldTermStructure ABC");
    ADD_BASE_BINDING(ql_termstructures::voltermstructure,
        "VolatilityTermStructure ABC");
    ADD_BASE_BINDING(ql_termstructures::blackvoltermstructure,
        "BlackVolTermStructure ABC");
    ADD_BASE_BINDING(ql_termstructures::localvoltermstructure,
        "LocalVolTermStructure ABC");

    // Handle types
    ADD_MAIN_BINDING(ql_termstructures::yieldtermstructurehandle,
        "Handle<YieldTermStructure>");
    ADD_MAIN_BINDING(ql_termstructures::relinkableyieldtermstructurehandle,
        "RelinkableHandle<YieldTermStructure>");
    ADD_MAIN_BINDING(ql_termstructures::blackvoltermstructurehandle,
        "Handle<BlackVolTermStructure>");
    ADD_MAIN_BINDING(ql_termstructures::relinkableblackvoltermstructurehandle,
        "RelinkableHandle<BlackVolTermStructure>");
    ADD_MAIN_BINDING(ql_termstructures::localvoltermstructurehandle,
        "Handle<LocalVolTermStructure>");
    ADD_MAIN_BINDING(ql_termstructures::relinkablelocalvoltermstructurehandle,
        "RelinkableHandle<LocalVolTermStructure>");

    // Enums
    ADD_MAIN_BINDING(ql_termstructures::volatilitytype,
        "VolatilityType - ShiftedLognormal or Normal");

    // Concrete implementations
    ADD_MAIN_BINDING(ql_termstructures::flatforward,
        "FlatForward yield curve");
    ADD_MAIN_BINDING(ql_termstructures::blackconstantvol,
        "BlackConstantVol volatility surface");
    ADD_MAIN_BINDING(ql_termstructures::blackvariancesurface,
        "BlackVarianceSurface volatility surface");
    ADD_MAIN_BINDING(ql_termstructures::localconstantvol,
        "LocalConstantVol volatility surface");
    ADD_MAIN_BINDING(ql_termstructures::localvolsurface,
        "LocalVolSurface from Black vol");
    ADD_MAIN_BINDING(ql_termstructures::fixedlocalvolsurface,
        "FixedLocalVolSurface with strike/time grid");
    ADD_MAIN_BINDING(ql_termstructures::noexceptlocalvolsurface,
        "NoExceptLocalVolSurface with fallback value");

    // Smile sections
    ADD_BASE_BINDING(ql_termstructures::smilesection,
        "SmileSection ABC");
    ADD_MAIN_BINDING(ql_termstructures::sabrsmilesection,
        "SabrSmileSection and SABR formula functions");
    ADD_MAIN_BINDING(ql_termstructures::sabrinterpolatedsmilesection,
        "SabrInterpolatedSmileSection - SABR calibration to market data");

    // Rate helpers and curve bootstrapping
    ADD_MAIN_BINDING(ql_termstructures::pillar,
        "Pillar enum");
    ADD_BASE_BINDING(ql_termstructures::ratehelper,
        "RateHelper, RelativeDateRateHelper ABCs");
    ADD_MAIN_BINDING(ql_termstructures::ratehelpers,
        "DepositRateHelper, FraRateHelper, SwapRateHelper");
    ADD_MAIN_BINDING(ql_termstructures::oisratehelper,
        "OISRateHelper");
    ADD_MAIN_BINDING(ql_termstructures::piecewiseyieldcurve,
        "PiecewiseYieldCurve instantiations");

    // Interpolated yield curves
    ADD_MAIN_BINDING(ql_termstructures::zerocurve,
        "ZeroCurve - zero rate curve with linear interpolation");
    ADD_MAIN_BINDING(ql_termstructures::discountcurve,
        "DiscountCurve - discount factor curve with log-linear interpolation");
    ADD_MAIN_BINDING(ql_termstructures::forwardcurve,
        "ForwardCurve - forward rate curve with backward-flat interpolation");
    ADD_MAIN_BINDING(ql_termstructures::zerospreadedtermstructure,
        "ZeroSpreadedTermStructure - yield curve with additive spread");
}
