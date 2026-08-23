/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2026 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/pricingengines/basket/pearsonspreadengine.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::pearsonspreadengine(py::module_& m) {
    py::class_<PearsonSpreadEngine, ext::shared_ptr<PearsonSpreadEngine>,
               SpreadBlackScholesVanillaEngine>(
        m, "PearsonSpreadEngine",
        "Pearson (1995) spread option engine using 1-D numerical integration.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Real, Real, Size, Real>(),
            py::arg("process1"), py::arg("process2"), py::arg("correlation"),
            py::arg("integrationTolerance") = 1e-10,
            py::arg("maxIntegrationIterations") = 10000,
            py::arg("nStd") = 8.0,
            "Constructs with two Black-Scholes processes, their correlation, "
            "and the integration controls.");
}
