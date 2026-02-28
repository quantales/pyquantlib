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
#include <ql/pricingengines/vanilla/analyticdividendeuropeanengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/cashflows/dividend.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticdividendeuropeanengine(py::module_& m) {
    py::class_<AnalyticDividendEuropeanEngine,
               ext::shared_ptr<AnalyticDividendEuropeanEngine>,
               PricingEngine>(
        m, "AnalyticDividendEuropeanEngine",
        "European engine with discrete dividends.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      DividendSchedule>(),
            py::arg("process"),
            py::arg("dividends"),
            "Constructs analytic dividend European engine.");
}
