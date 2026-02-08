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
#include <ql/instruments/creditdefaultswap.hpp>
#include <ql/instruments/claim.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::creditdefaultswap(py::module_& m) {
    py::class_<CreditDefaultSwap, Instrument,
               ext::shared_ptr<CreditDefaultSwap>>(
        m, "CreditDefaultSwap",
        "Credit default swap.")
        // Running-spread-only constructor
        .def(py::init([](Protection::Side side, Real notional, Rate spread,
                         const Schedule& schedule,
                         BusinessDayConvention paymentConvention,
                         const DayCounter& dayCounter,
                         bool settlesAccrual, bool paysAtDefaultTime,
                         const Date& protectionStart,
                         const py::object& lastPeriodDC,
                         bool rebatesAccrual,
                         const Date& tradeDate, Natural cashSettlementDays) {
            DayCounter lpdc;
            if (!lastPeriodDC.is_none())
                lpdc = lastPeriodDC.cast<DayCounter>();
            return ext::make_shared<CreditDefaultSwap>(
                side, notional, spread, schedule, paymentConvention,
                dayCounter, settlesAccrual, paysAtDefaultTime,
                protectionStart, ext::shared_ptr<Claim>(),
                lpdc, rebatesAccrual, tradeDate, cashSettlementDays);
        }),
            py::arg("side"),
            py::arg("notional"),
            py::arg("spread"),
            py::arg("schedule"),
            py::arg("paymentConvention"),
            py::arg("dayCounter"),
            py::arg("settlesAccrual") = true,
            py::arg("paysAtDefaultTime") = true,
            py::arg("protectionStart") = Date(),
            py::arg("lastPeriodDayCounter") = py::none(),
            py::arg("rebatesAccrual") = true,
            py::arg("tradeDate") = Date(),
            py::arg("cashSettlementDays") = 3,
            "Constructs CDS quoted as running spread only.")
        // Upfront + running-spread constructor
        .def(py::init([](Protection::Side side, Real notional,
                         Rate upfront, Rate spread,
                         const Schedule& schedule,
                         BusinessDayConvention paymentConvention,
                         const DayCounter& dayCounter,
                         bool settlesAccrual, bool paysAtDefaultTime,
                         const Date& protectionStart,
                         const Date& upfrontDate,
                         const py::object& lastPeriodDC,
                         bool rebatesAccrual,
                         const Date& tradeDate, Natural cashSettlementDays) {
            DayCounter lpdc;
            if (!lastPeriodDC.is_none())
                lpdc = lastPeriodDC.cast<DayCounter>();
            return ext::make_shared<CreditDefaultSwap>(
                side, notional, upfront, spread, schedule,
                paymentConvention, dayCounter, settlesAccrual,
                paysAtDefaultTime, protectionStart, upfrontDate,
                ext::shared_ptr<Claim>(), lpdc, rebatesAccrual,
                tradeDate, cashSettlementDays);
        }),
            py::arg("side"),
            py::arg("notional"),
            py::arg("upfront"),
            py::arg("spread"),
            py::arg("schedule"),
            py::arg("paymentConvention"),
            py::arg("dayCounter"),
            py::arg("settlesAccrual") = true,
            py::arg("paysAtDefaultTime") = true,
            py::arg("protectionStart") = Date(),
            py::arg("upfrontDate") = Date(),
            py::arg("lastPeriodDayCounter") = py::none(),
            py::arg("rebatesAccrual") = true,
            py::arg("tradeDate") = Date(),
            py::arg("cashSettlementDays") = 3,
            "Constructs CDS quoted as upfront and running spread.")
        // Inspectors
        .def("side", &CreditDefaultSwap::side, "Protection side.")
        .def("notional", &CreditDefaultSwap::notional, "Notional.")
        .def("runningSpread", &CreditDefaultSwap::runningSpread,
            "Running spread.")
        .def("settlesAccrual", &CreditDefaultSwap::settlesAccrual,
            "Whether accrual is settled on default.")
        .def("paysAtDefaultTime", &CreditDefaultSwap::paysAtDefaultTime,
            "Whether default payment is at default time.")
        .def("coupons", &CreditDefaultSwap::coupons, "Coupon leg.")
        .def("protectionStartDate",
            &CreditDefaultSwap::protectionStartDate,
            "Protection start date.")
        .def("protectionEndDate",
            &CreditDefaultSwap::protectionEndDate,
            "Protection end date.")
        .def("rebatesAccrual", &CreditDefaultSwap::rebatesAccrual,
            "Whether accrual is rebated.")
        .def("isExpired", &CreditDefaultSwap::isExpired,
            "Whether the CDS has expired.")
        // Results
        .def("fairUpfront", &CreditDefaultSwap::fairUpfront,
            "Fair upfront.")
        .def("fairSpread", &CreditDefaultSwap::fairSpread,
            "Fair running spread.")
        .def("couponLegBPS", &CreditDefaultSwap::couponLegBPS,
            "Coupon leg BPS.")
        .def("upfrontBPS", &CreditDefaultSwap::upfrontBPS,
            "Upfront BPS.")
        .def("couponLegNPV", &CreditDefaultSwap::couponLegNPV,
            "Coupon leg NPV.")
        .def("defaultLegNPV", &CreditDefaultSwap::defaultLegNPV,
            "Default leg NPV.")
        .def("upfrontNPV", &CreditDefaultSwap::upfrontNPV,
            "Upfront NPV.")
        .def("accrualRebateNPV", &CreditDefaultSwap::accrualRebateNPV,
            "Accrual rebate NPV.")
        .def("impliedHazardRate", &CreditDefaultSwap::impliedHazardRate,
            py::arg("targetNPV"),
            py::arg("discountCurve"),
            py::arg("dayCounter"),
            py::arg("recoveryRate") = 0.4,
            py::arg("accuracy") = 1.0e-8,
            py::arg("model") = CreditDefaultSwap::Midpoint,
            "Implied hazard rate.")
        .def("conventionalSpread",
            &CreditDefaultSwap::conventionalSpread,
            py::arg("conventionalRecovery"),
            py::arg("discountCurve"),
            py::arg("dayCounter"),
            py::arg("model") = CreditDefaultSwap::Midpoint,
            "Conventional spread.");

    // Free function
    m.def("cdsMaturity", &cdsMaturity,
        py::arg("tradeDate"), py::arg("tenor"), py::arg("rule"),
        "CDS maturity date from trade date and tenor.");
}
