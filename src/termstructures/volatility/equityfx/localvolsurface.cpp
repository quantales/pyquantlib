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
#include <ql/termstructures/volatility/equityfx/localvolsurface.hpp>
#include <ql/termstructures/volatility/equityfx/blackvoltermstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::localvolsurface(py::module_& m) {
    py::class_<LocalVolSurface, LocalVolTermStructure,
               ext::shared_ptr<LocalVolSurface>>(
        m, "LocalVolSurface",
        "Local volatility surface derived from a Black volatility surface.")
        // With quote handle for underlying
        .def(py::init<const Handle<BlackVolTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<Quote>&>(),
            py::arg("blackVolTS"),
            py::arg("riskFreeTS"),
            py::arg("dividendTS"),
            py::arg("underlying"),
            "Constructs from Black vol surface and quote handle for underlying.")
        // With fixed underlying value
        .def(py::init<const Handle<BlackVolTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      const Handle<YieldTermStructure>&,
                      Real>(),
            py::arg("blackVolTS"),
            py::arg("riskFreeTS"),
            py::arg("dividendTS"),
            py::arg("underlying"),
            "Constructs from Black vol surface and fixed underlying value.")
        // Hidden handles with quote for underlying
        .def(py::init([](const ext::shared_ptr<BlackVolTermStructure>& blackVolTS,
                         const ext::shared_ptr<YieldTermStructure>& riskFreeTS,
                         const ext::shared_ptr<YieldTermStructure>& dividendTS,
                         const ext::shared_ptr<Quote>& underlying) {
            return ext::make_shared<LocalVolSurface>(
                Handle<BlackVolTermStructure>(blackVolTS),
                Handle<YieldTermStructure>(riskFreeTS),
                Handle<YieldTermStructure>(dividendTS),
                Handle<Quote>(underlying));
        }), py::arg("blackVolTS"), py::arg("riskFreeTS"),
            py::arg("dividendTS"), py::arg("underlying"),
            "Constructs from term structures and quote (handles created internally).")
        // Hidden handles with fixed underlying value
        .def(py::init([](const ext::shared_ptr<BlackVolTermStructure>& blackVolTS,
                         const ext::shared_ptr<YieldTermStructure>& riskFreeTS,
                         const ext::shared_ptr<YieldTermStructure>& dividendTS,
                         Real underlying) {
            return ext::make_shared<LocalVolSurface>(
                Handle<BlackVolTermStructure>(blackVolTS),
                Handle<YieldTermStructure>(riskFreeTS),
                Handle<YieldTermStructure>(dividendTS),
                underlying);
        }), py::arg("blackVolTS"), py::arg("riskFreeTS"),
            py::arg("dividendTS"), py::arg("underlying"),
            "Constructs from term structures and fixed value (handles created internally).");
}
