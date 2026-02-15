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
#include <ql/termstructures/inflation/inflationhelpers.hpp>
#include <ql/quote.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::inflationhelpers(py::module_& m) {
    using RelZeroHelper =
        RelativeDateBootstrapHelper<ZeroInflationTermStructure>;

    // --- ZeroCouponInflationSwapHelper ---
    py::class_<ZeroCouponInflationSwapHelper, RelZeroHelper,
               ext::shared_ptr<ZeroCouponInflationSwapHelper>>(
        m, "ZeroCouponInflationSwapHelper",
        "Zero-coupon inflation swap bootstrap helper.")
        // Handle<Quote> constructor (non-deprecated, v1.39+)
        .def(py::init<const Handle<Quote>&,
                       const Period&,
                       const Date&,
                       Calendar,
                       BusinessDayConvention,
                       const DayCounter&,
                       const ext::shared_ptr<ZeroInflationIndex>&,
                       CPI::InterpolationType>(),
            py::arg("quote"),
            py::arg("swapObsLag"),
            py::arg("maturity"),
            py::arg("calendar"),
            py::arg("paymentConvention"),
            py::arg("dayCounter"),
            py::arg("zeroInflationIndex"),
            py::arg("observationInterpolation"),
            "Constructs from quote handle.")
        // shared_ptr<Quote> constructor (hidden handle)
        .def(py::init([](const ext::shared_ptr<Quote>& quote,
                         const Period& swapObsLag,
                         const Date& maturity,
                         Calendar calendar,
                         BusinessDayConvention paymentConvention,
                         const DayCounter& dayCounter,
                         const ext::shared_ptr<ZeroInflationIndex>& zii,
                         CPI::InterpolationType observationInterpolation) {
            return ext::make_shared<ZeroCouponInflationSwapHelper>(
                Handle<Quote>(quote), swapObsLag, maturity,
                std::move(calendar), paymentConvention, dayCounter,
                zii, observationInterpolation);
        }),
            py::arg("quote"),
            py::arg("swapObsLag"),
            py::arg("maturity"),
            py::arg("calendar"),
            py::arg("paymentConvention"),
            py::arg("dayCounter"),
            py::arg("zeroInflationIndex"),
            py::arg("observationInterpolation"),
            "Constructs from quote (handle created internally).")
        // Rate constructor
        .def(py::init([](Rate rate,
                         const Period& swapObsLag,
                         const Date& maturity,
                         Calendar calendar,
                         BusinessDayConvention paymentConvention,
                         const DayCounter& dayCounter,
                         const ext::shared_ptr<ZeroInflationIndex>& zii,
                         CPI::InterpolationType observationInterpolation) {
            return ext::make_shared<ZeroCouponInflationSwapHelper>(
                Handle<Quote>(ext::make_shared<SimpleQuote>(rate)),
                swapObsLag, maturity, std::move(calendar),
                paymentConvention, dayCounter, zii,
                observationInterpolation);
        }),
            py::arg("rate"),
            py::arg("swapObsLag"),
            py::arg("maturity"),
            py::arg("calendar"),
            py::arg("paymentConvention"),
            py::arg("dayCounter"),
            py::arg("zeroInflationIndex"),
            py::arg("observationInterpolation"),
            "Constructs from fixed rate.")
        .def("swap", &ZeroCouponInflationSwapHelper::swap,
            "Returns the underlying zero-coupon inflation swap.");

    using RelYoYHelper =
        RelativeDateBootstrapHelper<YoYInflationTermStructure>;

    // --- YearOnYearInflationSwapHelper ---
    py::class_<YearOnYearInflationSwapHelper, RelYoYHelper,
               ext::shared_ptr<YearOnYearInflationSwapHelper>>(
        m, "YearOnYearInflationSwapHelper",
        "Year-on-year inflation swap bootstrap helper.")
        // Handle<Quote> constructor
        .def(py::init<const Handle<Quote>&,
                       const Period&,
                       const Date&,
                       Calendar,
                       BusinessDayConvention,
                       DayCounter,
                       const ext::shared_ptr<YoYInflationIndex>&,
                       CPI::InterpolationType,
                       Handle<YieldTermStructure>>(),
            py::arg("quote"),
            py::arg("swapObsLag"),
            py::arg("maturity"),
            py::arg("calendar"),
            py::arg("paymentConvention"),
            py::arg("dayCounter"),
            py::arg("yoyInflationIndex"),
            py::arg("interpolation"),
            py::arg("nominalTermStructure"),
            "Constructs from quote handle.")
        // shared_ptr<Quote> constructor (hidden handle)
        .def(py::init([](const ext::shared_ptr<Quote>& quote,
                         const Period& swapObsLag,
                         const Date& maturity,
                         Calendar calendar,
                         BusinessDayConvention paymentConvention,
                         DayCounter dayCounter,
                         const ext::shared_ptr<YoYInflationIndex>& yii,
                         CPI::InterpolationType interpolation,
                         Handle<YieldTermStructure> nominalTermStructure) {
            return ext::make_shared<YearOnYearInflationSwapHelper>(
                Handle<Quote>(quote), swapObsLag, maturity,
                std::move(calendar), paymentConvention,
                std::move(dayCounter), yii, interpolation,
                std::move(nominalTermStructure));
        }),
            py::arg("quote"),
            py::arg("swapObsLag"),
            py::arg("maturity"),
            py::arg("calendar"),
            py::arg("paymentConvention"),
            py::arg("dayCounter"),
            py::arg("yoyInflationIndex"),
            py::arg("interpolation"),
            py::arg("nominalTermStructure"),
            "Constructs from quote (handle created internally).")
        // Rate constructor
        .def(py::init([](Rate rate,
                         const Period& swapObsLag,
                         const Date& maturity,
                         Calendar calendar,
                         BusinessDayConvention paymentConvention,
                         DayCounter dayCounter,
                         const ext::shared_ptr<YoYInflationIndex>& yii,
                         CPI::InterpolationType interpolation,
                         Handle<YieldTermStructure> nominalTermStructure) {
            return ext::make_shared<YearOnYearInflationSwapHelper>(
                Handle<Quote>(ext::make_shared<SimpleQuote>(rate)),
                swapObsLag, maturity, std::move(calendar),
                paymentConvention, std::move(dayCounter), yii,
                interpolation, std::move(nominalTermStructure));
        }),
            py::arg("rate"),
            py::arg("swapObsLag"),
            py::arg("maturity"),
            py::arg("calendar"),
            py::arg("paymentConvention"),
            py::arg("dayCounter"),
            py::arg("yoyInflationIndex"),
            py::arg("interpolation"),
            py::arg("nominalTermStructure"),
            "Constructs from fixed rate.")
        .def("swap", &YearOnYearInflationSwapHelper::swap,
            "Returns the underlying year-on-year inflation swap.");
}
