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
#include <ql/experimental/callablebonds/blackcallablebondengine.hpp>
#include <ql/experimental/callablebonds/callablebondvolstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_experimental::blackcallablebondengine(py::module_& m) {
    // BlackCallableFixedRateBondEngine
    py::class_<BlackCallableFixedRateBondEngine, PricingEngine,
               ext::shared_ptr<BlackCallableFixedRateBondEngine>>(
        m, "BlackCallableFixedRateBondEngine",
        "Black-formula callable fixed rate bond engine.")
        // Constructor: Handle<Quote> fwdYieldVol + Handle<YTS>
        .def(py::init<const Handle<Quote>&, Handle<YieldTermStructure>>(),
            py::arg("fwdYieldVol"),
            py::arg("discountCurve"),
            "Constructs with forward yield volatility quote and discount curve.")
        // Constructor: Handle<CallableBondVolatilityStructure> + Handle<YTS>
        .def(py::init<Handle<CallableBondVolatilityStructure>,
                      Handle<YieldTermStructure>>(),
            py::arg("yieldVolStructure"),
            py::arg("discountCurve"),
            "Constructs with callable bond volatility structure and discount curve.")
        // Hidden handle: shared_ptr<Quote> + shared_ptr<YTS>
        .def(py::init([](const ext::shared_ptr<Quote>& fwdYieldVol,
                         const ext::shared_ptr<YieldTermStructure>& discountCurve) {
            return ext::make_shared<BlackCallableFixedRateBondEngine>(
                Handle<Quote>(fwdYieldVol),
                Handle<YieldTermStructure>(discountCurve));
        }),
            py::arg("fwdYieldVol"),
            py::arg("discountCurve"),
            "Constructs with quote and term structure (handles created internally).")
        // Hidden handle: shared_ptr<CallableBondVolStructure> + shared_ptr<YTS>
        .def(py::init([](const ext::shared_ptr<CallableBondVolatilityStructure>& vol,
                         const ext::shared_ptr<YieldTermStructure>& discountCurve) {
            return ext::make_shared<BlackCallableFixedRateBondEngine>(
                Handle<CallableBondVolatilityStructure>(vol),
                Handle<YieldTermStructure>(discountCurve));
        }),
            py::arg("yieldVolStructure"),
            py::arg("discountCurve"),
            "Constructs with vol structure and term structure (handles created internally).");

    // BlackCallableZeroCouponBondEngine
    py::class_<BlackCallableZeroCouponBondEngine, BlackCallableFixedRateBondEngine,
               ext::shared_ptr<BlackCallableZeroCouponBondEngine>>(
        m, "BlackCallableZeroCouponBondEngine",
        "Black-formula callable zero coupon bond engine.")
        .def(py::init([](const ext::shared_ptr<Quote>& fwdYieldVol,
                         const ext::shared_ptr<YieldTermStructure>& discountCurve) {
            return ext::make_shared<BlackCallableZeroCouponBondEngine>(
                Handle<Quote>(fwdYieldVol),
                Handle<YieldTermStructure>(discountCurve));
        }),
            py::arg("fwdYieldVol"),
            py::arg("discountCurve"),
            "Constructs with quote and term structure (handles created internally).")
        .def(py::init<const Handle<Quote>&, const Handle<YieldTermStructure>&>(),
            py::arg("fwdYieldVol"),
            py::arg("discountCurve"),
            "Constructs with forward yield volatility quote handle and discount curve handle.");
}
