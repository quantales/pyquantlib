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
#include <ql/pricingengines/barrier/analyticsoftbarrierengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticsoftbarrierengine(py::module_& m) {
    py::class_<AnalyticSoftBarrierEngine, PricingEngine,
               ext::shared_ptr<AnalyticSoftBarrierEngine>>(
        m, "AnalyticSoftBarrierEngine",
        "Analytic soft barrier option engine.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>>(),
            py::arg("process"),
            "Constructs engine.");
}
