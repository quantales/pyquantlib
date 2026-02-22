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

DECLARE_MODULE_BINDINGS(cashflows_bindings) {
    // Abstract base classes
    ADD_BASE_BINDING(ql_cashflows::coupon, "Coupon ABC");
    ADD_BASE_BINDING(ql_cashflows::couponpricer_base,
        "FloatingRateCouponPricer ABC");

    // Concrete implementations
    ADD_MAIN_BINDING(ql_cashflows::simplecashflow, "SimpleCashFlow");
    ADD_MAIN_BINDING(ql_cashflows::fixedratecoupon, "FixedRateCoupon");
    ADD_MAIN_BINDING(ql_cashflows::floatingratecoupon,
        "FloatingRateCoupon");
    ADD_MAIN_BINDING(ql_cashflows::couponpricer,
        "BlackIborCouponPricer, setCouponPricer");
    ADD_MAIN_BINDING(ql_cashflows::rateaveraging,
        "RateAveraging enum");
    ADD_MAIN_BINDING(ql_cashflows::iborcoupon,
        "IborCoupon, IborLeg");
    ADD_MAIN_BINDING(ql_cashflows::overnightindexedcoupon,
        "OvernightIndexedCoupon, OvernightLeg");
    ADD_MAIN_BINDING(ql_cashflows::duration,
        "Duration::Type enum");

    // CMS support
    ADD_BASE_BINDING(ql_cashflows::cmscouponpricer,
        "CmsCouponPricer, MeanRevertingPricer ABCs");
    ADD_MAIN_BINDING(ql_cashflows::cmscoupon,
        "CmsCoupon, CmsLeg");
    ADD_MAIN_BINDING(ql_cashflows::lineartsrpricer,
        "LinearTsrPricer");

    // Inflation cashflows
    ADD_BASE_BINDING(ql_cashflows::inflationcoupon,
        "InflationCoupon ABC");
    ADD_MAIN_BINDING(ql_cashflows::zeroinflationcashflow,
        "ZeroInflationCashFlow");
    ADD_MAIN_BINDING(ql_cashflows::yoyinflationcoupon,
        "YoYInflationCoupon, yoyInflationLeg");
    ADD_MAIN_BINDING(ql_cashflows::capflooredinflationcoupon,
        "CappedFlooredYoYInflationCoupon");
    ADD_MAIN_BINDING(ql_cashflows::inflationcouponpricer,
        "InflationCouponPricer ABC, YoYInflationCouponPricer, "
        "Black/UnitDisplaced/Bachelier pricers");

    // Dividends
    ADD_MAIN_BINDING(ql_cashflows::dividend,
        "Dividend ABC, FixedDividend, FractionalDividend, DividendVector");
}
