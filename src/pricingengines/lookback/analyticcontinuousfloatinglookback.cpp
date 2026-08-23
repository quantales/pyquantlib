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
#include <ql/pricingengines/lookback/analyticcontinuousfloatinglookback.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticcontinuousfloatinglookbackengine(py::module_& m) {
    py::class_<AnalyticContinuousFloatingLookbackEngine,
               PricingEngine,
               ext::shared_ptr<AnalyticContinuousFloatingLookbackEngine>>(
        m, "AnalyticContinuousFloatingLookbackEngine",
        "Analytic engine for continuous floating-strike lookback options.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>>(),
             py::arg("process"));
}
