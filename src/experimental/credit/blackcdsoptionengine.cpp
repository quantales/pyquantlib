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
#include <ql/experimental/credit/blackcdsoptionengine.hpp>
#include <ql/termstructures/defaulttermstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_experimental::blackcdsoptionengine(py::module_& m) {
    py::class_<BlackCdsOptionEngine, PricingEngine,
               ext::shared_ptr<BlackCdsOptionEngine>>(
        m, "BlackCdsOptionEngine",
        "Black-formula CDS option engine.")
        // Handle-based constructor
        .def(py::init<Handle<DefaultProbabilityTermStructure>,
                      Real, Handle<YieldTermStructure>,
                      Handle<Quote>>(),
            py::arg("defaultProbTS"),
            py::arg("recoveryRate"),
            py::arg("termStructure"),
            py::arg("vol"),
            "Constructs the Black CDS option engine.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<DefaultProbabilityTermStructure>& defaultProbTS,
                         Real recoveryRate,
                         const ext::shared_ptr<YieldTermStructure>& termStructure,
                         const ext::shared_ptr<Quote>& vol) {
            return ext::make_shared<BlackCdsOptionEngine>(
                Handle<DefaultProbabilityTermStructure>(defaultProbTS),
                recoveryRate,
                Handle<YieldTermStructure>(termStructure),
                Handle<Quote>(vol));
        }),
            py::arg("defaultProbTS"),
            py::arg("recoveryRate"),
            py::arg("termStructure"),
            py::arg("vol"),
            "Constructs the Black CDS option engine (handles created internally).")
        .def("termStructure", &BlackCdsOptionEngine::termStructure,
            "Returns the term structure handle.")
        .def("volatility", &BlackCdsOptionEngine::volatility,
            "Returns the volatility handle.");
}
