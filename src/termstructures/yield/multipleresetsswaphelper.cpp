/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2026 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/termstructures/yield/multipleresetsswaphelper.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>
#include <variant>

namespace py = pybind11;
using namespace QuantLib;

namespace {

ext::shared_ptr<MultipleResetsSwapRateHelper> makeHelper(
    Natural settlementDays, const Period& tenor,
    const std::variant<Rate, Handle<Quote>>& fixedRate,
    const ext::shared_ptr<IborIndex>& iborIndex, Size resetsPerCoupon,
    const Handle<YieldTermStructure>& discountingCurve, RateAveraging::Type averagingMethod,
    Spread spread, Frequency fixedFrequency, const py::object& fixedDayCount,
    BusinessDayConvention fixedConvention) {
    DayCounter dc;
    if (!fixedDayCount.is_none())
        dc = fixedDayCount.cast<DayCounter>();
    return ext::make_shared<MultipleResetsSwapRateHelper>(
        settlementDays, tenor, fixedRate, iborIndex, resetsPerCoupon, discountingCurve,
        averagingMethod, spread, fixedFrequency, dc, fixedConvention);
}

}  // namespace

void ql_termstructures::multipleresetsswaphelper(py::module_& m) {
    py::class_<MultipleResetsSwapRateHelper, RelativeDateRateHelper,
               ext::shared_ptr<MultipleResetsSwapRateHelper>>(
        m, "MultipleResetsSwapRateHelper",
        "Rate helper bootstrapping from multiple-resets swap quotes.")
        // Fixed rate (numeric)
        .def(py::init([](Natural settlementDays, const Period& tenor, Rate fixedRate,
                         const ext::shared_ptr<IborIndex>& iborIndex, Size resetsPerCoupon,
                         const Handle<YieldTermStructure>& discountingCurve,
                         RateAveraging::Type averagingMethod, Spread spread,
                         Frequency fixedFrequency, const py::object& fixedDayCount,
                         BusinessDayConvention fixedConvention) {
            return makeHelper(settlementDays, tenor, fixedRate, iborIndex, resetsPerCoupon,
                              discountingCurve, averagingMethod, spread, fixedFrequency,
                              fixedDayCount, fixedConvention);
        }),
            py::arg("settlementDays"), py::arg("tenor"), py::arg("fixedRate"),
            py::arg("iborIndex"), py::arg("resetsPerCoupon"),
            py::arg("discountingCurve") = Handle<YieldTermStructure>(),
            py::arg("averagingMethod") = RateAveraging::Compound,
            py::arg("spread") = 0.0,
            py::arg("fixedFrequency") = NoFrequency,
            py::arg("fixedDayCount") = py::none(),
            py::arg("fixedConvention") = ModifiedFollowing,
            "Constructs from a fixed rate quote.")
        // Fixed rate (quote handle)
        .def(py::init([](Natural settlementDays, const Period& tenor,
                         const Handle<Quote>& fixedRate,
                         const ext::shared_ptr<IborIndex>& iborIndex, Size resetsPerCoupon,
                         const Handle<YieldTermStructure>& discountingCurve,
                         RateAveraging::Type averagingMethod, Spread spread,
                         Frequency fixedFrequency, const py::object& fixedDayCount,
                         BusinessDayConvention fixedConvention) {
            return makeHelper(settlementDays, tenor, fixedRate, iborIndex, resetsPerCoupon,
                              discountingCurve, averagingMethod, spread, fixedFrequency,
                              fixedDayCount, fixedConvention);
        }),
            py::arg("settlementDays"), py::arg("tenor"), py::arg("fixedRate"),
            py::arg("iborIndex"), py::arg("resetsPerCoupon"),
            py::arg("discountingCurve") = Handle<YieldTermStructure>(),
            py::arg("averagingMethod") = RateAveraging::Compound,
            py::arg("spread") = 0.0,
            py::arg("fixedFrequency") = NoFrequency,
            py::arg("fixedDayCount") = py::none(),
            py::arg("fixedConvention") = ModifiedFollowing,
            "Constructs from a fixed rate quote handle.")
        // Fixed rate (hidden quote handle)
        .def(py::init([](Natural settlementDays, const Period& tenor,
                         const ext::shared_ptr<Quote>& fixedRate,
                         const ext::shared_ptr<IborIndex>& iborIndex, Size resetsPerCoupon,
                         const Handle<YieldTermStructure>& discountingCurve,
                         RateAveraging::Type averagingMethod, Spread spread,
                         Frequency fixedFrequency, const py::object& fixedDayCount,
                         BusinessDayConvention fixedConvention) {
            return makeHelper(settlementDays, tenor, Handle<Quote>(fixedRate), iborIndex,
                              resetsPerCoupon, discountingCurve, averagingMethod, spread,
                              fixedFrequency, fixedDayCount, fixedConvention);
        }),
            py::arg("settlementDays"), py::arg("tenor"), py::arg("fixedRate"),
            py::arg("iborIndex"), py::arg("resetsPerCoupon"),
            py::arg("discountingCurve") = Handle<YieldTermStructure>(),
            py::arg("averagingMethod") = RateAveraging::Compound,
            py::arg("spread") = 0.0,
            py::arg("fixedFrequency") = NoFrequency,
            py::arg("fixedDayCount") = py::none(),
            py::arg("fixedConvention") = ModifiedFollowing,
            "Constructs from a fixed rate quote (handle created internally).");
}
