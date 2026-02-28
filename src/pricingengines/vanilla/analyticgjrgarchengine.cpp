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
#include <ql/pricingengines/vanilla/analyticgjrgarchengine.hpp>
#include <ql/models/equity/gjrgarchmodel.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticgjrgarchengine(py::module_& m) {
    py::class_<AnalyticGJRGARCHEngine, PricingEngine,
               ext::shared_ptr<AnalyticGJRGARCHEngine>>(
        m, "AnalyticGJRGARCHEngine",
        "Analytic GJR-GARCH option engine.")
        .def(py::init<const ext::shared_ptr<GJRGARCHModel>&>(),
             py::arg("model"));
}
