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
#include <ql/termstructures/yield/oisratehelper.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::oisratehelper(py::module_& m) {
    py::class_<OISRateHelper, RelativeDateRateHelper,
               ext::shared_ptr<OISRateHelper>>(
        m, "OISRateHelper",
        "Rate helper for bootstrapping over OIS rates.")
        // Rate + tenor (most common)
        .def(py::init([](Natural settlementDays, const Period& tenor,
                         Rate fixedRate,
                         const ext::shared_ptr<OvernightIndex>& overnightIndex,
                         const Handle<YieldTermStructure>& discountingCurve,
                         bool telescopicValueDates,
                         Integer paymentLag,
                         BusinessDayConvention paymentConvention,
                         Frequency paymentFrequency,
                         const py::object& paymentCalendar,
                         const Period& forwardStart,
                         Spread overnightSpread,
                         Pillar::Choice pillar,
                         const Date& customPillarDate,
                         RateAveraging::Type averagingMethod,
                         const py::object& lookbackDays,
                         Natural lockoutDays,
                         bool applyObservationShift) {
            Calendar payCal;
            if (!paymentCalendar.is_none())
                payCal = paymentCalendar.cast<Calendar>();
            Natural lb = Null<Natural>();
            if (!lookbackDays.is_none())
                lb = lookbackDays.cast<Natural>();
            return ext::make_shared<OISRateHelper>(
                settlementDays, tenor, fixedRate, overnightIndex,
                discountingCurve, telescopicValueDates, paymentLag,
                paymentConvention, paymentFrequency, payCal,
                forwardStart, overnightSpread, pillar, customPillarDate,
                averagingMethod, ext::nullopt, ext::nullopt,
                Calendar(), lb, lockoutDays, applyObservationShift);
        }),
             py::arg("settlementDays"), py::arg("tenor"),
             py::arg("fixedRate"), py::arg("overnightIndex"),
             py::arg("discountingCurve") = Handle<YieldTermStructure>(),
             py::arg("telescopicValueDates") = false,
             py::arg("paymentLag") = 0,
             py::arg("paymentConvention") = Following,
             py::arg("paymentFrequency") = Annual,
             py::arg("paymentCalendar") = py::none(),
             py::arg("forwardStart") = Period(0, Days),
             py::arg("overnightSpread") = 0.0,
             py::arg("pillar") = Pillar::LastRelevantDate,
             py::arg("customPillarDate") = Date(),
             py::arg("averagingMethod") = RateAveraging::Compound,
             py::arg("lookbackDays") = py::none(),
             py::arg("lockoutDays") = 0,
             py::arg("applyObservationShift") = false,
             "Constructs from settlement days, tenor, and overnight index.")
        // Handle<Quote> + tenor
        .def(py::init([](Natural settlementDays, const Period& tenor,
                         const Handle<Quote>& fixedRate,
                         const ext::shared_ptr<OvernightIndex>& overnightIndex,
                         const Handle<YieldTermStructure>& discountingCurve,
                         bool telescopicValueDates,
                         Integer paymentLag,
                         BusinessDayConvention paymentConvention,
                         Frequency paymentFrequency,
                         const py::object& paymentCalendar,
                         const Period& forwardStart,
                         Spread overnightSpread,
                         Pillar::Choice pillar,
                         const Date& customPillarDate,
                         RateAveraging::Type averagingMethod,
                         const py::object& lookbackDays,
                         Natural lockoutDays,
                         bool applyObservationShift) {
            Calendar payCal;
            if (!paymentCalendar.is_none())
                payCal = paymentCalendar.cast<Calendar>();
            Natural lb = Null<Natural>();
            if (!lookbackDays.is_none())
                lb = lookbackDays.cast<Natural>();
            return ext::make_shared<OISRateHelper>(
                settlementDays, tenor, fixedRate, overnightIndex,
                discountingCurve, telescopicValueDates, paymentLag,
                paymentConvention, paymentFrequency, payCal,
                forwardStart, overnightSpread, pillar, customPillarDate,
                averagingMethod, ext::nullopt, ext::nullopt,
                Calendar(), lb, lockoutDays, applyObservationShift);
        }),
             py::arg("settlementDays"), py::arg("tenor"),
             py::arg("fixedRate"), py::arg("overnightIndex"),
             py::arg("discountingCurve") = Handle<YieldTermStructure>(),
             py::arg("telescopicValueDates") = false,
             py::arg("paymentLag") = 0,
             py::arg("paymentConvention") = Following,
             py::arg("paymentFrequency") = Annual,
             py::arg("paymentCalendar") = py::none(),
             py::arg("forwardStart") = Period(0, Days),
             py::arg("overnightSpread") = 0.0,
             py::arg("pillar") = Pillar::LastRelevantDate,
             py::arg("customPillarDate") = Date(),
             py::arg("averagingMethod") = RateAveraging::Compound,
             py::arg("lookbackDays") = py::none(),
             py::arg("lockoutDays") = 0,
             py::arg("applyObservationShift") = false,
             "Constructs from settlement days, tenor, and quote handle.")
        // shared_ptr<Quote> + tenor (hidden handle)
        .def(py::init([](Natural settlementDays, const Period& tenor,
                         const ext::shared_ptr<Quote>& fixedRate,
                         const ext::shared_ptr<OvernightIndex>& overnightIndex,
                         const Handle<YieldTermStructure>& discountingCurve,
                         bool telescopicValueDates,
                         Integer paymentLag,
                         BusinessDayConvention paymentConvention,
                         Frequency paymentFrequency,
                         const py::object& paymentCalendar,
                         const Period& forwardStart,
                         Spread overnightSpread,
                         Pillar::Choice pillar,
                         const Date& customPillarDate,
                         RateAveraging::Type averagingMethod,
                         const py::object& lookbackDays,
                         Natural lockoutDays,
                         bool applyObservationShift) {
            Calendar payCal;
            if (!paymentCalendar.is_none())
                payCal = paymentCalendar.cast<Calendar>();
            Natural lb = Null<Natural>();
            if (!lookbackDays.is_none())
                lb = lookbackDays.cast<Natural>();
            return ext::make_shared<OISRateHelper>(
                settlementDays, tenor, Handle<Quote>(fixedRate),
                overnightIndex, discountingCurve, telescopicValueDates,
                paymentLag, paymentConvention, paymentFrequency, payCal,
                forwardStart, overnightSpread, pillar, customPillarDate,
                averagingMethod, ext::nullopt, ext::nullopt,
                Calendar(), lb, lockoutDays, applyObservationShift);
        }),
             py::arg("settlementDays"), py::arg("tenor"),
             py::arg("fixedRate"), py::arg("overnightIndex"),
             py::arg("discountingCurve") = Handle<YieldTermStructure>(),
             py::arg("telescopicValueDates") = false,
             py::arg("paymentLag") = 0,
             py::arg("paymentConvention") = Following,
             py::arg("paymentFrequency") = Annual,
             py::arg("paymentCalendar") = py::none(),
             py::arg("forwardStart") = Period(0, Days),
             py::arg("overnightSpread") = 0.0,
             py::arg("pillar") = Pillar::LastRelevantDate,
             py::arg("customPillarDate") = Date(),
             py::arg("averagingMethod") = RateAveraging::Compound,
             py::arg("lookbackDays") = py::none(),
             py::arg("lockoutDays") = 0,
             py::arg("applyObservationShift") = false,
             "Constructs from settlement days, tenor, and quote (handle created internally).")
        .def("swap", &OISRateHelper::swap,
             "Returns the underlying OIS swap.");
}
