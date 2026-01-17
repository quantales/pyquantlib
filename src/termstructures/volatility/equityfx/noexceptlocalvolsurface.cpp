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
#include <ql/termstructures/volatility/equityfx/noexceptlocalvolsurface.hpp>
#include <ql/termstructures/volatility/equityfx/blackvoltermstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::noexceptlocalvolsurface(py::module_& m) {
    py::class_<NoExceptLocalVolSurface, LocalVolSurface,
               ext::shared_ptr<NoExceptLocalVolSurface>>(
        m, "NoExceptLocalVolSurface",
        "Local volatility surface that returns a fallback value instead of throwing.")
        // With quote handle for underlying
        .def(py::init<const Handle<BlackVolTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<Quote>&,
                      Real>(),
            py::arg("blackTS"),
            py::arg("riskFreeTS"),
            py::arg("dividendTS"),
            py::arg("underlying"),
            py::arg("illegalLocalVolOverwrite"),
            "Constructs with quote handle for underlying.")
        // With fixed underlying value
        .def(py::init<const Handle<BlackVolTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      Real,
                      Real>(),
            py::arg("blackTS"),
            py::arg("riskFreeTS"),
            py::arg("dividendTS"),
            py::arg("underlying"),
            py::arg("illegalLocalVolOverwrite"),
            "Constructs with fixed underlying value.")
        // Hidden handles with quote for underlying
        .def(py::init([](const ext::shared_ptr<BlackVolTermStructure>& blackTS,
                         const ext::shared_ptr<YieldTermStructure>& riskFreeTS,
                         const ext::shared_ptr<YieldTermStructure>& dividendTS,
                         const ext::shared_ptr<Quote>& underlying,
                         Real illegalLocalVolOverwrite) {
            return ext::make_shared<NoExceptLocalVolSurface>(
                Handle<BlackVolTermStructure>(blackTS),
                Handle<YieldTermStructure>(riskFreeTS),
                Handle<YieldTermStructure>(dividendTS),
                Handle<Quote>(underlying),
                illegalLocalVolOverwrite);
        }), py::arg("blackTS"), py::arg("riskFreeTS"),
            py::arg("dividendTS"), py::arg("underlying"),
            py::arg("illegalLocalVolOverwrite"),
            "Constructs from term structures and quote (handles created internally).")
        // Hidden handles with fixed underlying value
        .def(py::init([](const ext::shared_ptr<BlackVolTermStructure>& blackTS,
                         const ext::shared_ptr<YieldTermStructure>& riskFreeTS,
                         const ext::shared_ptr<YieldTermStructure>& dividendTS,
                         Real underlying,
                         Real illegalLocalVolOverwrite) {
            return ext::make_shared<NoExceptLocalVolSurface>(
                Handle<BlackVolTermStructure>(blackTS),
                Handle<YieldTermStructure>(riskFreeTS),
                Handle<YieldTermStructure>(dividendTS),
                underlying,
                illegalLocalVolOverwrite);
        }), py::arg("blackTS"), py::arg("riskFreeTS"),
            py::arg("dividendTS"), py::arg("underlying"),
            py::arg("illegalLocalVolOverwrite"),
            "Constructs from term structures and fixed value (handles created internally).");
}
