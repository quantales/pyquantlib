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

DECLARE_MODULE_BINDINGS(instruments_bindings) {
    auto m = manager.module();

    manager.addFunction(ql_instruments::swap, m,
        "Swap - interest rate swap base class");
    manager.addFunction(ql_instruments::strikedtypepayoff, m,
        "StrikedTypePayoff - payoff with strike and option type");
    manager.addFunction(ql_instruments::payoffs, m,
        "PlainVanillaPayoff - plain vanilla option payoffs");
    manager.addFunction(ql_instruments::oneassetoption, m,
        "OneAssetOption - base class for single-asset options");
    manager.addFunction(ql_instruments::vanillaoption, m,
        "VanillaOption - plain vanilla options");
    manager.addFunction(ql_instruments::multiassetoption, m,
        "MultiAssetOption - base class for multi-asset options");
    manager.addFunction(ql_instruments::basketoption, m,
        "BasketOption - basket options and payoffs");
}
