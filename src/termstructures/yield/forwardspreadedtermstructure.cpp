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
#include <ql/termstructures/yield/forwardspreadedtermstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::forwardspreadedtermstructure(py::module_& m) {
    py::class_<ForwardSpreadedTermStructure, YieldTermStructure,
               ext::shared_ptr<ForwardSpreadedTermStructure>>(
        m, "ForwardSpreadedTermStructure",
        "Yield curve with an additive spread on forward rates.")
        // Handle constructor
        .def(py::init<Handle<YieldTermStructure>, Handle<Quote>>(),
            py::arg("curveHandle"), py::arg("spreadHandle"),
            "Constructs from yield curve and spread handles.")
        // Hidden handle
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& curve,
                         const ext::shared_ptr<Quote>& spread) {
            return ext::make_shared<ForwardSpreadedTermStructure>(
                Handle<YieldTermStructure>(curve),
                Handle<Quote>(spread));
        }),
            py::arg("curve"), py::arg("spread"),
            "Constructs from yield curve and spread (handles created internally).");
}
