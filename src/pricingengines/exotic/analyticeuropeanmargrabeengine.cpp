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
#include <ql/pricingengines/exotic/analyticeuropeanmargrabeengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticeuropeanmargrabeengine(py::module_& m) {
    py::class_<AnalyticEuropeanMargrabeEngine,
               PricingEngine,
               ext::shared_ptr<AnalyticEuropeanMargrabeEngine>>(
        m, "AnalyticEuropeanMargrabeEngine",
        "Analytic engine for European exchange (Margrabe) options.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Real>(),
             py::arg("process1"),
             py::arg("process2"),
             py::arg("correlation"));
}
