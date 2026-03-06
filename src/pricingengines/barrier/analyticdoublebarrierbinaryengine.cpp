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
#include <ql/pricingengines/barrier/analyticdoublebarrierbinaryengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticdoublebarrierbinaryengine(py::module_& m) {
    py::class_<AnalyticDoubleBarrierBinaryEngine, PricingEngine,
               ext::shared_ptr<AnalyticDoubleBarrierBinaryEngine>>(
        m, "AnalyticDoubleBarrierBinaryEngine",
        "Analytic double barrier binary (one-touch) option engine (Hui).")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>>(),
            py::arg("process"),
            "Constructs AnalyticDoubleBarrierBinaryEngine.");
}
