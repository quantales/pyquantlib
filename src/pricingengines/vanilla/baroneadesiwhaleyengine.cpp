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
#include <ql/pricingengines/vanilla/baroneadesiwhaleyengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::baroneadesiwhaleyengine(py::module_& m) {
    py::class_<BaroneAdesiWhaleyApproximationEngine,
               ext::shared_ptr<BaroneAdesiWhaleyApproximationEngine>,
               PricingEngine>(
        m, "BaroneAdesiWhaleyApproximationEngine",
        "Barone-Adesi and Whaley approximation engine for American options (1987).")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>>(),
            py::arg("process"),
            "Constructs from a Black-Scholes process.")
        .def_static("criticalPrice",
            &BaroneAdesiWhaleyApproximationEngine::criticalPrice,
            py::arg("payoff"),
            py::arg("riskFreeDiscount"),
            py::arg("dividendDiscount"),
            py::arg("variance"),
            py::arg("tolerance") = 1e-6,
            "Computes the critical price for early exercise.");
}
