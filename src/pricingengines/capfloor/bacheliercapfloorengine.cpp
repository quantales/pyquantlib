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
#include <ql/pricingengines/capfloor/bacheliercapfloorengine.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::bacheliercapfloorengine(py::module_& m) {
    py::class_<BachelierCapFloorEngine, PricingEngine,
               ext::shared_ptr<BachelierCapFloorEngine>>(
        m, "BachelierCapFloorEngine",
        "Bachelier (normal) cap/floor engine.")
        // Scalar volatility constructor
        .def(py::init<Handle<YieldTermStructure>, Volatility,
                      const DayCounter&>(),
            py::arg("discountCurve"),
            py::arg("vol"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with flat normal volatility (handle).")
        // Hidden handle: scalar vol
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& disc,
                        Volatility vol, const DayCounter& dc) {
            return ext::make_shared<BachelierCapFloorEngine>(
                Handle<YieldTermStructure>(disc), vol, dc);
        }),
            py::arg("discountCurve"),
            py::arg("vol"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with flat normal volatility.")
        // Quote handle constructor
        .def(py::init<Handle<YieldTermStructure>, const Handle<Quote>&,
                      const DayCounter&>(),
            py::arg("discountCurve"),
            py::arg("vol"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with quote normal volatility (handle).")
        // Hidden handle: Quote
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& disc,
                        const ext::shared_ptr<Quote>& vol,
                        const DayCounter& dc) {
            return ext::make_shared<BachelierCapFloorEngine>(
                Handle<YieldTermStructure>(disc),
                Handle<Quote>(vol), dc);
        }),
            py::arg("discountCurve"),
            py::arg("vol"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with quote normal volatility.");
}
