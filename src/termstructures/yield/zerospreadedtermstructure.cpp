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
#include <ql/termstructures/yield/zerospreadedtermstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::zerospreadedtermstructure(py::module_& m) {
    py::class_<ZeroSpreadedTermStructure, YieldTermStructure,
               ext::shared_ptr<ZeroSpreadedTermStructure>>(
        m, "ZeroSpreadedTermStructure",
        "Yield curve with an additive spread on zero rates.")
        // Handle constructor
        .def(py::init<Handle<YieldTermStructure>, Handle<Quote>,
                      Compounding, Frequency>(),
            py::arg("curveHandle"), py::arg("spreadHandle"),
            py::arg("compounding") = Continuous,
            py::arg("frequency") = NoFrequency,
            "Constructs from yield curve and spread handles.")
        // Hidden handle: shared_ptr overload
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& curve,
                         const ext::shared_ptr<Quote>& spread,
                         Compounding compounding,
                         Frequency frequency) {
            return ext::make_shared<ZeroSpreadedTermStructure>(
                Handle<YieldTermStructure>(curve),
                Handle<Quote>(spread),
                compounding, frequency);
        }),
            py::arg("curve"), py::arg("spread"),
            py::arg("compounding") = Continuous,
            py::arg("frequency") = NoFrequency,
            "Constructs from yield curve and spread (handles created internally).");
}
