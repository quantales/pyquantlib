/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 *
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 *
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#include "pyquantlib/pyquantlib.h"
#include "pyquantlib/binding_manager.h"

DECLARE_MODULE_BINDINGS(instruments_bindings) {
    auto m = manager.module();

    manager.addFunction(ql_instruments::strikedtypepayoff, m,
        "StrikedTypePayoff - payoff with strike and option type");
    manager.addFunction(ql_instruments::payoffs, m,
        "PlainVanillaPayoff - plain vanilla option payoffs");
    manager.addFunction(ql_instruments::oneassetoption, m,
        "OneAssetOption - base class for single-asset options");
    manager.addFunction(ql_instruments::vanillaoption, m,
        "VanillaOption - plain vanilla options");
}
