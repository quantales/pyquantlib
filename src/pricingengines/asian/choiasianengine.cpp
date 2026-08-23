/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/pricingengines/asian/choiasianengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::choiasianengine(py::module_& m) {
    py::class_<ChoiAsianEngine,
               PricingEngine,
               ext::shared_ptr<ChoiAsianEngine>>(
        m, "ChoiAsianEngine",
        "Choi (2018) discrete arithmetic Asian option engine.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Real, Size>(),
            py::arg("process"),
            py::arg("lambda") = 15.0,
            py::arg("maxNrIntegrationSteps") = 2 << 21,
            "Constructs engine.");
}
