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
#include <ql/pricingengines/vanilla/analyticeuropeanengine.hpp>
#include <ql/instruments/oneassetoption.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticeuropeanengine(py::module_& m) {
    py::class_<AnalyticEuropeanEngine, OneAssetOption::engine,
               ext::shared_ptr<AnalyticEuropeanEngine>>(
        m, "AnalyticEuropeanEngine",
        "Analytic pricing engine for European vanilla options.")
        .def(py::init<const ext::shared_ptr<GeneralizedBlackScholesProcess>&>(),
             py::arg("process"),
            "Constructs engine with a Black-Scholes process.")
        .def(py::init<const ext::shared_ptr<GeneralizedBlackScholesProcess>&,
                      const Handle<YieldTermStructure>&>(),
             py::arg("process"), py::arg("discountCurve"),
            "Constructs engine with separate discount curve.");
}
