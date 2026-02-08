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
#include <ql/termstructures/credit/defaultprobabilityhelpers.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::defaultprobabilityhelper(py::module_& m) {
    // DefaultProbabilityHelper base class
    py::class_<DefaultProbabilityHelper,
               ext::shared_ptr<DefaultProbabilityHelper>,
               Observer, Observable>(
        m, "DefaultProbabilityHelper",
        "Bootstrap helper for default probability term structures.")
        .def("impliedQuote", &DefaultProbabilityHelper::impliedQuote,
            "Returns the implied quote.")
        .def("earliestDate", &DefaultProbabilityHelper::earliestDate,
            "Returns the earliest date.")
        .def("maturityDate", &DefaultProbabilityHelper::maturityDate,
            "Returns the maturity date.")
        .def("latestDate", &DefaultProbabilityHelper::latestDate,
            "Returns the latest date.")
        .def("latestRelevantDate",
            &DefaultProbabilityHelper::latestRelevantDate,
            "Returns the latest relevant date.");
}

void ql_termstructures::defaultprobabilityhelpers(py::module_& m) {
    // SpreadCdsHelper
    py::class_<SpreadCdsHelper, DefaultProbabilityHelper,
               ext::shared_ptr<SpreadCdsHelper>>(
        m, "SpreadCdsHelper",
        "Spread-quoted CDS bootstrap helper.")
        // Constructor with Rate
        .def(py::init([](Rate runningSpread, const Period& tenor,
                         Integer settlementDays, const Calendar& calendar,
                         Frequency frequency,
                         BusinessDayConvention paymentConvention,
                         DateGeneration::Rule rule,
                         const DayCounter& dayCounter,
                         Real recoveryRate,
                         const Handle<YieldTermStructure>& discountCurve,
                         bool settlesAccrual, bool paysAtDefaultTime,
                         const Date& startDate,
                         const py::object& lastPeriodDC,
                         bool rebatesAccrual,
                         CreditDefaultSwap::PricingModel model) {
            DayCounter lpdc;
            if (!lastPeriodDC.is_none())
                lpdc = lastPeriodDC.cast<DayCounter>();
            return ext::make_shared<SpreadCdsHelper>(
                runningSpread, tenor, settlementDays, calendar,
                frequency, paymentConvention, rule, dayCounter,
                recoveryRate, discountCurve, settlesAccrual,
                paysAtDefaultTime, startDate, lpdc,
                rebatesAccrual, model);
        }),
            py::arg("runningSpread"),
            py::arg("tenor"),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("frequency"),
            py::arg("paymentConvention"),
            py::arg("rule"),
            py::arg("dayCounter"),
            py::arg("recoveryRate"),
            py::arg("discountCurve"),
            py::arg("settlesAccrual") = true,
            py::arg("paysAtDefaultTime") = true,
            py::arg("startDate") = Date(),
            py::arg("lastPeriodDayCounter") = py::none(),
            py::arg("rebatesAccrual") = true,
            py::arg("model") = CreditDefaultSwap::Midpoint,
            "Constructs from running spread.")
        // Constructor with Quote handle
        .def(py::init([](const Handle<Quote>& runningSpread,
                         const Period& tenor,
                         Integer settlementDays, const Calendar& calendar,
                         Frequency frequency,
                         BusinessDayConvention paymentConvention,
                         DateGeneration::Rule rule,
                         const DayCounter& dayCounter,
                         Real recoveryRate,
                         const Handle<YieldTermStructure>& discountCurve,
                         bool settlesAccrual, bool paysAtDefaultTime,
                         const Date& startDate,
                         const py::object& lastPeriodDC,
                         bool rebatesAccrual,
                         CreditDefaultSwap::PricingModel model) {
            DayCounter lpdc;
            if (!lastPeriodDC.is_none())
                lpdc = lastPeriodDC.cast<DayCounter>();
            return ext::make_shared<SpreadCdsHelper>(
                runningSpread, tenor, settlementDays, calendar,
                frequency, paymentConvention, rule, dayCounter,
                recoveryRate, discountCurve, settlesAccrual,
                paysAtDefaultTime, startDate, lpdc,
                rebatesAccrual, model);
        }),
            py::arg("runningSpread"),
            py::arg("tenor"),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("frequency"),
            py::arg("paymentConvention"),
            py::arg("rule"),
            py::arg("dayCounter"),
            py::arg("recoveryRate"),
            py::arg("discountCurve"),
            py::arg("settlesAccrual") = true,
            py::arg("paysAtDefaultTime") = true,
            py::arg("startDate") = Date(),
            py::arg("lastPeriodDayCounter") = py::none(),
            py::arg("rebatesAccrual") = true,
            py::arg("model") = CreditDefaultSwap::Midpoint,
            "Constructs from running spread quote.");

    // UpfrontCdsHelper
    py::class_<UpfrontCdsHelper, DefaultProbabilityHelper,
               ext::shared_ptr<UpfrontCdsHelper>>(
        m, "UpfrontCdsHelper",
        "Upfront-quoted CDS bootstrap helper.")
        // Constructor with Rate upfront
        .def(py::init([](Rate upfront, Rate runningSpread,
                         const Period& tenor,
                         Integer settlementDays, const Calendar& calendar,
                         Frequency frequency,
                         BusinessDayConvention paymentConvention,
                         DateGeneration::Rule rule,
                         const DayCounter& dayCounter,
                         Real recoveryRate,
                         const Handle<YieldTermStructure>& discountCurve,
                         Natural upfrontSettlementDays,
                         bool settlesAccrual, bool paysAtDefaultTime,
                         const Date& startDate,
                         const py::object& lastPeriodDC,
                         bool rebatesAccrual,
                         CreditDefaultSwap::PricingModel model) {
            DayCounter lpdc;
            if (!lastPeriodDC.is_none())
                lpdc = lastPeriodDC.cast<DayCounter>();
            return ext::make_shared<UpfrontCdsHelper>(
                upfront, runningSpread, tenor, settlementDays, calendar,
                frequency, paymentConvention, rule, dayCounter,
                recoveryRate, discountCurve, upfrontSettlementDays,
                settlesAccrual, paysAtDefaultTime, startDate,
                lpdc, rebatesAccrual, model);
        }),
            py::arg("upfront"),
            py::arg("runningSpread"),
            py::arg("tenor"),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("frequency"),
            py::arg("paymentConvention"),
            py::arg("rule"),
            py::arg("dayCounter"),
            py::arg("recoveryRate"),
            py::arg("discountCurve"),
            py::arg("upfrontSettlementDays") = 3,
            py::arg("settlesAccrual") = true,
            py::arg("paysAtDefaultTime") = true,
            py::arg("startDate") = Date(),
            py::arg("lastPeriodDayCounter") = py::none(),
            py::arg("rebatesAccrual") = true,
            py::arg("model") = CreditDefaultSwap::Midpoint,
            "Constructs from upfront and running spread.")
        // Constructor with Quote handle upfront
        .def(py::init([](const Handle<Quote>& upfront, Rate runningSpread,
                         const Period& tenor,
                         Integer settlementDays, const Calendar& calendar,
                         Frequency frequency,
                         BusinessDayConvention paymentConvention,
                         DateGeneration::Rule rule,
                         const DayCounter& dayCounter,
                         Real recoveryRate,
                         const Handle<YieldTermStructure>& discountCurve,
                         Natural upfrontSettlementDays,
                         bool settlesAccrual, bool paysAtDefaultTime,
                         const Date& startDate,
                         const py::object& lastPeriodDC,
                         bool rebatesAccrual,
                         CreditDefaultSwap::PricingModel model) {
            DayCounter lpdc;
            if (!lastPeriodDC.is_none())
                lpdc = lastPeriodDC.cast<DayCounter>();
            return ext::make_shared<UpfrontCdsHelper>(
                upfront, runningSpread, tenor, settlementDays, calendar,
                frequency, paymentConvention, rule, dayCounter,
                recoveryRate, discountCurve, upfrontSettlementDays,
                settlesAccrual, paysAtDefaultTime, startDate,
                lpdc, rebatesAccrual, model);
        }),
            py::arg("upfront"),
            py::arg("runningSpread"),
            py::arg("tenor"),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("frequency"),
            py::arg("paymentConvention"),
            py::arg("rule"),
            py::arg("dayCounter"),
            py::arg("recoveryRate"),
            py::arg("discountCurve"),
            py::arg("upfrontSettlementDays") = 3,
            py::arg("settlesAccrual") = true,
            py::arg("paysAtDefaultTime") = true,
            py::arg("startDate") = Date(),
            py::arg("lastPeriodDayCounter") = py::none(),
            py::arg("rebatesAccrual") = true,
            py::arg("model") = CreditDefaultSwap::Midpoint,
            "Constructs from upfront quote and running spread.");
}
