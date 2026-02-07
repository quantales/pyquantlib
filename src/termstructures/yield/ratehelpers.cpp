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
#include <ql/termstructures/yield/ratehelpers.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::pillar(py::module_& m) {
    // Pillar enum (from bootstraphelper.hpp)
    py::class_<Pillar> pillar(m, "Pillar",
        "Pillar date calculation types for rate helpers.");
    py::enum_<Pillar::Choice>(pillar, "Choice",
        "Pillar choice for rate helper.")
        .value("MaturityDate", Pillar::MaturityDate,
            "Use the instrument maturity date.")
        .value("LastRelevantDate", Pillar::LastRelevantDate,
            "Use the last relevant date for pricing.")
        .value("CustomDate", Pillar::CustomDate,
            "Use a custom pillar date.");
}

void ql_termstructures::ratehelper(py::module_& m) {
    // RateHelper base class (typedef for BootstrapHelper<YieldTermStructure>)
    py::class_<RateHelper, ext::shared_ptr<RateHelper>, Observer, Observable>(
        m, "RateHelper",
        "Rate helper for bootstrapping yield curves.")
        .def("quote", &RateHelper::quote,
             "Returns the market quote handle.")
        .def("impliedQuote", &RateHelper::impliedQuote,
             "Returns the implied quote from the term structure.")
        .def("quoteError", &RateHelper::quoteError,
             "Returns the difference between market and implied quotes.")
        .def("pillarDate", &RateHelper::pillarDate,
             "Returns the pillar date.")
        .def("earliestDate", &RateHelper::earliestDate,
             "Returns the earliest date.")
        .def("maturityDate", &RateHelper::maturityDate,
             "Returns the maturity date.")
        .def("latestDate", &RateHelper::latestDate,
             "Returns the latest date.")
        .def("latestRelevantDate", &RateHelper::latestRelevantDate,
             "Returns the latest relevant date.");

    // RelativeDateRateHelper (typedef for RelativeDateBootstrapHelper<YieldTermStructure>)
    py::class_<RelativeDateRateHelper, RateHelper,
               ext::shared_ptr<RelativeDateRateHelper>>(
        m, "RelativeDateRateHelper",
        "Rate helper with date schedule relative to evaluation date.");
}

void ql_termstructures::ratehelpers(py::module_& m) {
    // --- DepositRateHelper ---
    py::class_<DepositRateHelper, RelativeDateRateHelper,
               ext::shared_ptr<DepositRateHelper>>(
        m, "DepositRateHelper",
        "Rate helper for bootstrapping over deposit rates.")
        // Rate + IborIndex
        .def(py::init([](Rate rate,
                         const ext::shared_ptr<IborIndex>& index) {
            return ext::make_shared<DepositRateHelper>(rate, index);
        }), py::arg("rate"), py::arg("index"),
            "Constructs from rate and Ibor index.")
        // Handle<Quote> + IborIndex
        .def(py::init([](const Handle<Quote>& rate,
                         const ext::shared_ptr<IborIndex>& index) {
            return ext::make_shared<DepositRateHelper>(rate, index);
        }), py::arg("rate"), py::arg("index"),
            "Constructs from quote handle and Ibor index.")
        // shared_ptr<Quote> + IborIndex (hidden handle)
        .def(py::init([](const ext::shared_ptr<Quote>& rate,
                         const ext::shared_ptr<IborIndex>& index) {
            return ext::make_shared<DepositRateHelper>(
                Handle<Quote>(rate), index);
        }), py::arg("rate"), py::arg("index"),
            "Constructs from quote and Ibor index (handle created internally).")
        // Rate + full params
        .def(py::init([](Rate rate, const Period& tenor, Natural fixingDays,
                         const Calendar& calendar,
                         BusinessDayConvention convention,
                         bool endOfMonth, const DayCounter& dayCounter) {
            return ext::make_shared<DepositRateHelper>(
                rate, tenor, fixingDays, calendar,
                convention, endOfMonth, dayCounter);
        }), py::arg("rate"), py::arg("tenor"), py::arg("fixingDays"),
            py::arg("calendar"), py::arg("convention"),
            py::arg("endOfMonth"), py::arg("dayCounter"),
            "Constructs from rate and explicit market conventions.");

    // --- FraRateHelper ---
    py::class_<FraRateHelper, RelativeDateRateHelper,
               ext::shared_ptr<FraRateHelper>>(
        m, "FraRateHelper",
        "Rate helper for bootstrapping over FRA rates.")
        // Rate + monthsToStart + IborIndex
        .def(py::init([](Rate rate, Natural monthsToStart,
                         const ext::shared_ptr<IborIndex>& index,
                         Pillar::Choice pillar,
                         const Date& customPillarDate,
                         bool useIndexedCoupon) {
            return ext::make_shared<FraRateHelper>(
                rate, monthsToStart, index,
                pillar, customPillarDate, useIndexedCoupon);
        }), py::arg("rate"), py::arg("monthsToStart"),
            py::arg("index"),
            py::arg("pillar") = Pillar::LastRelevantDate,
            py::arg("customPillarDate") = Date(),
            py::arg("useIndexedCoupon") = true,
            "Constructs from rate, months to start, and Ibor index.")
        // Handle<Quote> + monthsToStart + IborIndex
        .def(py::init([](const Handle<Quote>& rate, Natural monthsToStart,
                         const ext::shared_ptr<IborIndex>& index,
                         Pillar::Choice pillar,
                         const Date& customPillarDate,
                         bool useIndexedCoupon) {
            return ext::make_shared<FraRateHelper>(
                rate, monthsToStart, index,
                pillar, customPillarDate, useIndexedCoupon);
        }), py::arg("rate"), py::arg("monthsToStart"),
            py::arg("index"),
            py::arg("pillar") = Pillar::LastRelevantDate,
            py::arg("customPillarDate") = Date(),
            py::arg("useIndexedCoupon") = true,
            "Constructs from quote handle, months to start, and Ibor index.")
        // shared_ptr<Quote> + monthsToStart + IborIndex (hidden handle)
        .def(py::init([](const ext::shared_ptr<Quote>& rate,
                         Natural monthsToStart,
                         const ext::shared_ptr<IborIndex>& index,
                         Pillar::Choice pillar,
                         const Date& customPillarDate,
                         bool useIndexedCoupon) {
            return ext::make_shared<FraRateHelper>(
                Handle<Quote>(rate), monthsToStart, index,
                pillar, customPillarDate, useIndexedCoupon);
        }), py::arg("rate"), py::arg("monthsToStart"),
            py::arg("index"),
            py::arg("pillar") = Pillar::LastRelevantDate,
            py::arg("customPillarDate") = Date(),
            py::arg("useIndexedCoupon") = true,
            "Constructs from quote, months to start, and Ibor index (handle created internally).")
        // Rate + Period + IborIndex
        .def(py::init([](Rate rate, const Period& periodToStart,
                         const ext::shared_ptr<IborIndex>& index,
                         Pillar::Choice pillar,
                         const Date& customPillarDate,
                         bool useIndexedCoupon) {
            return ext::make_shared<FraRateHelper>(
                rate, periodToStart, index,
                pillar, customPillarDate, useIndexedCoupon);
        }), py::arg("rate"), py::arg("periodToStart"),
            py::arg("index"),
            py::arg("pillar") = Pillar::LastRelevantDate,
            py::arg("customPillarDate") = Date(),
            py::arg("useIndexedCoupon") = true,
            "Constructs from rate, period to start, and Ibor index.");

    // --- SwapRateHelper ---
    py::class_<SwapRateHelper, RelativeDateRateHelper,
               ext::shared_ptr<SwapRateHelper>>(
        m, "SwapRateHelper",
        "Rate helper for bootstrapping over swap rates.")
        // Rate + tenor (most common)
        .def(py::init([](Rate rate, const Period& tenor,
                         const Calendar& calendar,
                         Frequency fixedFrequency,
                         BusinessDayConvention fixedConvention,
                         const DayCounter& fixedDayCount,
                         const ext::shared_ptr<IborIndex>& iborIndex,
                         const Handle<Quote>& spread,
                         const Period& fwdStart,
                         const Handle<YieldTermStructure>& discountingCurve,
                         const py::object& settlementDays,
                         Pillar::Choice pillar,
                         const Date& customPillarDate,
                         bool endOfMonth) {
            Natural sd = Null<Natural>();
            if (!settlementDays.is_none())
                sd = settlementDays.cast<Natural>();
            return ext::make_shared<SwapRateHelper>(
                rate, tenor, calendar, fixedFrequency, fixedConvention,
                fixedDayCount, iborIndex, spread, fwdStart,
                discountingCurve, sd, pillar, customPillarDate, endOfMonth);
        }),
             py::arg("rate"), py::arg("tenor"),
             py::arg("calendar"),
             py::arg("fixedFrequency"), py::arg("fixedConvention"),
             py::arg("fixedDayCount"), py::arg("iborIndex"),
             py::arg("spread") = Handle<Quote>(),
             py::arg("fwdStart") = Period(0, Days),
             py::arg("discountingCurve") = Handle<YieldTermStructure>(),
             py::arg("settlementDays") = py::none(),
             py::arg("pillar") = Pillar::LastRelevantDate,
             py::arg("customPillarDate") = Date(),
             py::arg("endOfMonth") = false,
             "Constructs from rate, tenor, and market conventions.")
        // Handle<Quote> + tenor
        .def(py::init([](const Handle<Quote>& rate, const Period& tenor,
                         const Calendar& calendar,
                         Frequency fixedFrequency,
                         BusinessDayConvention fixedConvention,
                         const DayCounter& fixedDayCount,
                         const ext::shared_ptr<IborIndex>& iborIndex,
                         const Handle<Quote>& spread,
                         const Period& fwdStart,
                         const Handle<YieldTermStructure>& discountingCurve,
                         const py::object& settlementDays,
                         Pillar::Choice pillar,
                         const Date& customPillarDate,
                         bool endOfMonth) {
            Natural sd = Null<Natural>();
            if (!settlementDays.is_none())
                sd = settlementDays.cast<Natural>();
            return ext::make_shared<SwapRateHelper>(
                rate, tenor, calendar, fixedFrequency, fixedConvention,
                fixedDayCount, iborIndex, spread, fwdStart,
                discountingCurve, sd, pillar, customPillarDate, endOfMonth);
        }),
             py::arg("rate"), py::arg("tenor"),
             py::arg("calendar"),
             py::arg("fixedFrequency"), py::arg("fixedConvention"),
             py::arg("fixedDayCount"), py::arg("iborIndex"),
             py::arg("spread") = Handle<Quote>(),
             py::arg("fwdStart") = Period(0, Days),
             py::arg("discountingCurve") = Handle<YieldTermStructure>(),
             py::arg("settlementDays") = py::none(),
             py::arg("pillar") = Pillar::LastRelevantDate,
             py::arg("customPillarDate") = Date(),
             py::arg("endOfMonth") = false,
             "Constructs from quote handle, tenor, and market conventions.")
        // shared_ptr<Quote> + tenor (hidden handle)
        .def(py::init([](const ext::shared_ptr<Quote>& rate,
                         const Period& tenor,
                         const Calendar& calendar,
                         Frequency fixedFrequency,
                         BusinessDayConvention fixedConvention,
                         const DayCounter& fixedDayCount,
                         const ext::shared_ptr<IborIndex>& iborIndex,
                         const Handle<Quote>& spread,
                         const Period& fwdStart,
                         const Handle<YieldTermStructure>& discountingCurve,
                         const py::object& settlementDays,
                         Pillar::Choice pillar,
                         const Date& customPillarDate,
                         bool endOfMonth) {
            Natural sd = Null<Natural>();
            if (!settlementDays.is_none())
                sd = settlementDays.cast<Natural>();
            return ext::make_shared<SwapRateHelper>(
                Handle<Quote>(rate), tenor, calendar,
                fixedFrequency, fixedConvention, fixedDayCount,
                iborIndex, spread, fwdStart,
                discountingCurve, sd, pillar, customPillarDate, endOfMonth);
        }),
             py::arg("rate"), py::arg("tenor"),
             py::arg("calendar"),
             py::arg("fixedFrequency"), py::arg("fixedConvention"),
             py::arg("fixedDayCount"), py::arg("iborIndex"),
             py::arg("spread") = Handle<Quote>(),
             py::arg("fwdStart") = Period(0, Days),
             py::arg("discountingCurve") = Handle<YieldTermStructure>(),
             py::arg("settlementDays") = py::none(),
             py::arg("pillar") = Pillar::LastRelevantDate,
             py::arg("customPillarDate") = Date(),
             py::arg("endOfMonth") = false,
             "Constructs from quote, tenor, and market conventions (handle created internally).")
        .def("spread", &SwapRateHelper::spread,
             "Returns the spread.")
        .def("swap", &SwapRateHelper::swap,
             "Returns the underlying swap.")
        .def("forwardStart", &SwapRateHelper::forwardStart,
             py::return_value_policy::reference_internal,
             "Returns the forward start period.");
}
