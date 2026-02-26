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
#include <ql/pricingengines/forward/forwardengine.hpp>
#include <ql/pricingengines/forward/forwardperformanceengine.hpp>
#include <ql/pricingengines/vanilla/analyticeuropeanengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::forwardengine(py::module_& m) {
    using ForwardEuropeanEngine =
        ForwardVanillaEngine<AnalyticEuropeanEngine>;

    py::class_<ForwardEuropeanEngine, PricingEngine,
               ext::shared_ptr<ForwardEuropeanEngine>>(
        m, "ForwardEuropeanEngine",
        "Forward-start European option engine (Black-Scholes).")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>>(),
             py::arg("process"));

    using ForwardPerformanceEuropeanEngine =
        ForwardPerformanceVanillaEngine<AnalyticEuropeanEngine>;

    py::class_<ForwardPerformanceEuropeanEngine, PricingEngine,
               ext::shared_ptr<ForwardPerformanceEuropeanEngine>>(
        m, "ForwardPerformanceEuropeanEngine",
        "Forward-start performance European option engine.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>>(),
             py::arg("process"));
}
