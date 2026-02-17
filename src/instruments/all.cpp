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
    ADD_MAIN_BINDING(ql_instruments::overnightindexedswap,
        "OvernightIndexedSwap - OIS swap");
    ADD_MAIN_BINDING(ql_instruments::makeois,
        "MakeOIS - helper for constructing OIS");
    ADD_MAIN_BINDING(ql_instruments::capfloor,
        "CapFloor - interest rate caps, floors, and collars");
    ADD_MAIN_BINDING(ql_instruments::makecapfloor,
        "MakeCapFloor - helper for constructing caps and floors");
    ADD_MAIN_BINDING(ql_instruments::makevanillaswap,
        "MakeVanillaSwap - helper for constructing vanilla swaps");
    ADD_MAIN_BINDING(ql_instruments::forwardrateagreement,
        "ForwardRateAgreement - FRA instrument");
    ADD_MAIN_BINDING(ql_instruments::barriertype,
        "BarrierType - barrier type enum");
    ADD_MAIN_BINDING(ql_instruments::barrieroption,
        "BarrierOption - barrier option on a single asset");
    ADD_MAIN_BINDING(ql_instruments::doublebarriertype,
        "DoubleBarrierType - double barrier type enum");
    ADD_MAIN_BINDING(ql_instruments::doublebarrieroption,
        "DoubleBarrierOption - double barrier option on a single asset");
    ADD_MAIN_BINDING(ql_instruments::averagetype,
        "AverageType - averaging type enum");
    ADD_MAIN_BINDING(ql_instruments::asianoption,
        "AsianOption - Asian options with averaging");
    ADD_MAIN_BINDING(ql_instruments::makeswaption,
        "MakeSwaption - helper for constructing swaptions");
    ADD_MAIN_BINDING(ql_instruments::zerocouponswap,
        "ZeroCouponSwap - zero-coupon interest rate swap");
    ADD_MAIN_BINDING(ql_instruments::compositeinstrument,
        "CompositeInstrument - aggregate of weighted instruments");
    ADD_MAIN_BINDING(ql_instruments::assetswap,
        "AssetSwap - bullet bond vs Libor swap");
    ADD_MAIN_BINDING(ql_instruments::claim,
        "Claim, FaceValueClaim, FaceValueAccrualClaim");
    ADD_MAIN_BINDING(ql_instruments::creditdefaultswap,
        "CreditDefaultSwap - credit default swap");

    // Inflation instruments
    ADD_MAIN_BINDING(ql_instruments::zerocouponinflationswap,
        "ZeroCouponInflationSwap");
    ADD_MAIN_BINDING(ql_instruments::yearonyearinflationswap,
        "YearOnYearInflationSwap");
    ADD_MAIN_BINDING(ql_instruments::inflationcapfloor,
        "YoYInflationCapFloor, Cap, Floor, Collar");
    ADD_MAIN_BINDING(ql_instruments::makeyoyinflationcapfloor,
        "MakeYoYInflationCapFloor builder");
}
