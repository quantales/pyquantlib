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
#include <ql/pricingengines/barrier/analyticdoublebarrierengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticdoublebarrierengine(py::module_& m) {
    py::class_<AnalyticDoubleBarrierEngine, PricingEngine,
               ext::shared_ptr<AnalyticDoubleBarrierEngine>>(
        m, "AnalyticDoubleBarrierEngine",
        "Analytic double barrier option engine (Ikeda-Kunitomo).")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>, int>(),
            py::arg("process"),
            py::arg("series") = 5,
            "Constructs AnalyticDoubleBarrierEngine.");
}
