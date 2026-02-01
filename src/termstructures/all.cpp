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
    auto m = manager.module();
    auto b = manager.getSubmodule("base");

    // Abstract base classes
    manager.addFunction(ql_termstructures::yieldtermstructure, b,
        "YieldTermStructure ABC");
    manager.addFunction(ql_termstructures::voltermstructure, b,
        "VolatilityTermStructure ABC");
    manager.addFunction(ql_termstructures::blackvoltermstructure, b,
        "BlackVolTermStructure ABC");
    manager.addFunction(ql_termstructures::localvoltermstructure, b,
        "LocalVolTermStructure ABC");

    // Handle types
    manager.addFunction(ql_termstructures::yieldtermstructurehandle, m,
        "Handle<YieldTermStructure>");
    manager.addFunction(ql_termstructures::relinkableyieldtermstructurehandle, m,
        "RelinkableHandle<YieldTermStructure>");
    manager.addFunction(ql_termstructures::blackvoltermstructurehandle, m,
        "Handle<BlackVolTermStructure>");
    manager.addFunction(ql_termstructures::relinkableblackvoltermstructurehandle, m,
        "RelinkableHandle<BlackVolTermStructure>");
    manager.addFunction(ql_termstructures::localvoltermstructurehandle, m,
        "Handle<LocalVolTermStructure>");
    manager.addFunction(ql_termstructures::relinkablelocalvoltermstructurehandle, m,
        "RelinkableHandle<LocalVolTermStructure>");

    // Enums
    manager.addFunction(ql_termstructures::volatilitytype, m,
        "VolatilityType - ShiftedLognormal or Normal");

    // Concrete implementations
    manager.addFunction(ql_termstructures::flatforward, m,
        "FlatForward yield curve");
    manager.addFunction(ql_termstructures::blackconstantvol, m,
        "BlackConstantVol volatility surface");
    manager.addFunction(ql_termstructures::blackvariancesurface, m,
        "BlackVarianceSurface volatility surface");
    manager.addFunction(ql_termstructures::localconstantvol, m,
        "LocalConstantVol volatility surface");
    manager.addFunction(ql_termstructures::localvolsurface, m,
        "LocalVolSurface from Black vol");
    manager.addFunction(ql_termstructures::fixedlocalvolsurface, m,
        "FixedLocalVolSurface with strike/time grid");
    manager.addFunction(ql_termstructures::noexceptlocalvolsurface, m,
        "NoExceptLocalVolSurface with fallback value");

    // Smile sections
    manager.addFunction(ql_termstructures::smilesection, b,
        "SmileSection ABC");
}
