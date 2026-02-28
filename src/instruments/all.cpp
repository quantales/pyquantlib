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
    ADD_MAIN_BINDING(ql_instruments::amortizingfixedratebond,
        "AmortizingFixedRateBond - amortizing fixed rate bond");
    ADD_MAIN_BINDING(ql_instruments::amortizingfloatingratebond,
        "AmortizingFloatingRateBond - amortizing floating rate bond");
    ADD_MAIN_BINDING(ql_instruments::cmsratebond,
        "CmsRateBond - CMS rate bond");
    ADD_MAIN_BINDING(ql_instruments::amortizingcmsratebond,
        "AmortizingCmsRateBond - amortizing CMS rate bond");
    ADD_MAIN_BINDING(ql_instruments::cpibond,
        "CPIBond - CPI inflation-linked bond");
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

    ADD_MAIN_BINDING(ql_instruments::bondforward,
        "BondForward - forward contract on a bond");
    ADD_MAIN_BINDING(ql_instruments::varianceswap,
        "VarianceSwap - variance swap instrument");
    ADD_MAIN_BINDING(ql_instruments::nonstandardswap,
        "NonstandardSwap - swap with period-dependent parameters");
    ADD_MAIN_BINDING(ql_instruments::nonstandardswaption,
        "NonstandardSwaption - option on nonstandard swap");
    ADD_MAIN_BINDING(ql_instruments::floatfloatswap,
        "FloatFloatSwap - float vs float swap with caps and floors");
    ADD_MAIN_BINDING(ql_instruments::floatfloatswaption,
        "FloatFloatSwaption - option on float-float swap");
    ADD_MAIN_BINDING(ql_instruments::equitytotalreturnswap,
        "EquityTotalReturnSwap - equity total return swap");
    ADD_MAIN_BINDING(ql_instruments::callability,
        "Callability - call/put schedule entry");
    ADD_MAIN_BINDING(ql_instruments::convertiblebonds,
        "ConvertibleBond, ConvertibleZeroCouponBond, "
        "ConvertibleFixedCouponBond, ConvertibleFloatingRateBond, SoftCallability");

    // Lookback options
    ADD_MAIN_BINDING(ql_instruments::lookbackoption,
        "ContinuousFloatingLookbackOption, ContinuousFixedLookbackOption, "
        "ContinuousPartialFloatingLookbackOption, ContinuousPartialFixedLookbackOption");
    ADD_MAIN_BINDING(ql_instruments::cliquetoption,
        "CliquetOption - cliquet (ratchet) option");
    ADD_MAIN_BINDING(ql_instruments::compoundoption,
        "CompoundOption - option on an option");
    ADD_MAIN_BINDING(ql_instruments::simplechooseroption,
        "SimpleChooserOption - simple chooser option");
    ADD_MAIN_BINDING(ql_instruments::complexchooseroption,
        "ComplexChooserOption - complex chooser option");
    ADD_MAIN_BINDING(ql_instruments::quantovanillaoption,
        "QuantoVanillaOption - quanto vanilla option");
    ADD_MAIN_BINDING(ql_instruments::margrabeoption,
        "MargrabeOption - exchange option (Margrabe)");
    ADD_MAIN_BINDING(ql_instruments::forwardvanillaoption,
        "ForwardVanillaOption - forward-start vanilla option");
    ADD_MAIN_BINDING(ql_instruments::quantoforwardvanillaoption,
        "QuantoForwardVanillaOption - quanto forward-start option");
    // Extensible options
    ADD_MAIN_BINDING(ql_instruments::holderextensibleoption,
        "HolderExtensibleOption - holder-extensible option");
    ADD_MAIN_BINDING(ql_instruments::writerextensibleoption,
        "WriterExtensibleOption - writer-extensible option");
}
