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
#include "pyquantlib/trampolines.h"
#include <ql/pricingengine.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::pricingengine(py::module_& m) {
    auto pyPricingEngine = py::class_<PricingEngine, PyPricingEngine,
        ext::shared_ptr<PricingEngine>, Observable>(m, "PricingEngine",
        "Abstract base class for pricing engines.")
        .def(py::init_alias<>())
        .def("getArguments", &PricingEngine::getArguments,
            py::return_value_policy::reference,
            "Returns a pointer to the arguments structure.")
        .def("getResults", &PricingEngine::getResults,
            py::return_value_policy::reference,
            "Returns a pointer to the results structure.")
        .def("reset", &PricingEngine::reset,
            "Resets the engine results.")
        .def("calculate", &PricingEngine::calculate,
            "Performs the calculation.");

    py::class_<PricingEngine::arguments, PyPricingEngineArguments,
        ext::shared_ptr<PricingEngine::arguments>>(pyPricingEngine, "arguments",
        "Abstract base class for pricing engine arguments.")
        .def(py::init<>())
        .def("validate", &PricingEngine::arguments::validate,
            "Validates the arguments.");

    py::class_<PricingEngine::results, PyPricingEngineResults,
        ext::shared_ptr<PricingEngine::results>>(pyPricingEngine, "results",
        "Abstract base class for pricing engine results.")
        .def(py::init<>())
        .def("reset", &PricingEngine::results::reset,
            "Resets the results.");
}
