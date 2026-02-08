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
#include <ql/pricingengines/swaption/blackswaptionengine.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::blackswaptionengine(py::module_& m) {
    using BSE = BlackSwaptionEngine;

    py::class_<BSE, PricingEngine, ext::shared_ptr<BSE>>(
        m, "BlackSwaptionEngine",
        "Shifted lognormal Black-formula swaption engine.")
        // Constructor: constant volatility (hidden handle)
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& discountCurve,
                         Volatility vol,
                         const DayCounter& dc,
                         Real displacement) {
            return ext::make_shared<BSE>(
                Handle<YieldTermStructure>(discountCurve),
                vol, dc, displacement);
        }),
            py::arg("discountCurve"),
            py::arg("vol"),
            py::arg("dayCounter") = Actual365Fixed(),
            py::arg("displacement") = 0.0,
            "Constructs from constant volatility.")
        // Constructor: quote volatility (hidden handle)
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& discountCurve,
                         const ext::shared_ptr<Quote>& vol,
                         const DayCounter& dc,
                         Real displacement) {
            return ext::make_shared<BSE>(
                Handle<YieldTermStructure>(discountCurve),
                Handle<Quote>(vol), dc, displacement);
        }),
            py::arg("discountCurve"),
            py::arg("vol"),
            py::arg("dayCounter") = Actual365Fixed(),
            py::arg("displacement") = 0.0,
            "Constructs from quote volatility.")
        // Constructor: explicit handles (constant vol)
        .def(py::init<const Handle<YieldTermStructure>&, Volatility,
                       const DayCounter&, Real>(),
            py::arg("discountCurve"),
            py::arg("vol"),
            py::arg("dayCounter") = Actual365Fixed(),
            py::arg("displacement") = 0.0,
            "Constructs from constant volatility (handle).")
        // Constructor: explicit handles (quote vol)
        .def(py::init<const Handle<YieldTermStructure>&, const Handle<Quote>&,
                       const DayCounter&, Real>(),
            py::arg("discountCurve"),
            py::arg("vol"),
            py::arg("dayCounter") = Actual365Fixed(),
            py::arg("displacement") = 0.0,
            "Constructs from quote volatility (handle).");

    // BachelierSwaptionEngine - normal vol swaption engine
    using BachSE = BachelierSwaptionEngine;

    py::class_<BachSE, PricingEngine, ext::shared_ptr<BachSE>>(
        m, "BachelierSwaptionEngine",
        "Normal Bachelier-formula swaption engine.")
        // Constructor: constant volatility (hidden handle)
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& discountCurve,
                         Volatility vol,
                         const DayCounter& dc) {
            return ext::make_shared<BachSE>(
                Handle<YieldTermStructure>(discountCurve), vol, dc);
        }),
            py::arg("discountCurve"),
            py::arg("vol"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs from constant normal volatility.")
        // Constructor: quote volatility (hidden handle)
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& discountCurve,
                         const ext::shared_ptr<Quote>& vol,
                         const DayCounter& dc) {
            return ext::make_shared<BachSE>(
                Handle<YieldTermStructure>(discountCurve),
                Handle<Quote>(vol), dc);
        }),
            py::arg("discountCurve"),
            py::arg("vol"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs from quote normal volatility.")
        // Constructor: explicit handles (constant vol)
        .def(py::init<const Handle<YieldTermStructure>&, Volatility,
                       const DayCounter&>(),
            py::arg("discountCurve"),
            py::arg("vol"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs from constant normal volatility (handle).")
        // Constructor: explicit handles (quote vol)
        .def(py::init<const Handle<YieldTermStructure>&, const Handle<Quote>&,
                       const DayCounter&>(),
            py::arg("discountCurve"),
            py::arg("vol"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs from quote normal volatility (handle).");
}
