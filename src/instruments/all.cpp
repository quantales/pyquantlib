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
    ADD_MAIN_BINDING(ql_instruments::bond,
        "Bond - base class for bonds");
    ADD_MAIN_BINDING(ql_instruments::fixedratebond,
        "FixedRateBond - fixed rate bond");
    ADD_MAIN_BINDING(ql_instruments::zerocouponbond,
        "ZeroCouponBond - zero coupon bond");
    ADD_MAIN_BINDING(ql_instruments::floatingratebond,
        "FloatingRateBond - floating rate bond");
    ADD_MAIN_BINDING(ql_instruments::swap,
        "Swap - interest rate swap base class");
    ADD_MAIN_BINDING(ql_instruments::fixedvsfloatingswap,
        "FixedVsFloatingSwap - fixed vs floating swap base class");
    ADD_MAIN_BINDING(ql_instruments::vanillaswap,
        "VanillaSwap - fixed vs floating swap");
    ADD_MAIN_BINDING(ql_instruments::swaption,
        "Swaption - option to enter a swap");
    ADD_MAIN_BINDING(ql_instruments::strikedtypepayoff,
        "StrikedTypePayoff - payoff with strike and option type");
    ADD_MAIN_BINDING(ql_instruments::payoffs,
        "PlainVanillaPayoff - plain vanilla option payoffs");
    ADD_MAIN_BINDING(ql_instruments::oneassetoption,
        "OneAssetOption - base class for single-asset options");
    ADD_MAIN_BINDING(ql_instruments::vanillaoption,
        "VanillaOption - plain vanilla options");
    ADD_MAIN_BINDING(ql_instruments::multiassetoption,
        "MultiAssetOption - base class for multi-asset options");
    ADD_MAIN_BINDING(ql_instruments::basketoption,
        "BasketOption - basket options and payoffs");
}
