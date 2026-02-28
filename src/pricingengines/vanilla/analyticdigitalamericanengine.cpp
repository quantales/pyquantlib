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
#include <ql/pricingengines/vanilla/analyticdigitalamericanengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticdigitalamericanengine(py::module_& m) {
    py::class_<AnalyticDigitalAmericanEngine,
               ext::shared_ptr<AnalyticDigitalAmericanEngine>,
               PricingEngine>(
        m, "AnalyticDigitalAmericanEngine",
        "Analytic pricing engine for digital American options (knock-in).")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>>(),
            py::arg("process"),
            "Constructs analytic digital American engine.");

    py::class_<AnalyticDigitalAmericanKOEngine,
               ext::shared_ptr<AnalyticDigitalAmericanKOEngine>,
               AnalyticDigitalAmericanEngine>(
        m, "AnalyticDigitalAmericanKOEngine",
        "Analytic pricing engine for digital American options (knock-out).")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>>(),
            py::arg("process"),
            "Constructs analytic digital American knock-out engine.");
}
