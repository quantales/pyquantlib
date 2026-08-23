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
#include <ql/pricingengines/vanilla/analyticeuropeanvasicekengine.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticeuropeanvasicekengine(py::module_& m) {
    py::class_<AnalyticBlackVasicekEngine, PricingEngine,
               ext::shared_ptr<AnalyticBlackVasicekEngine>>(
        m, "AnalyticBlackVasicekEngine",
        "European option engine with stochastic Vasicek interest rates.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      ext::shared_ptr<Vasicek>,
                      Real>(),
            py::arg("bsProcess"),
            py::arg("vasicekProcess"),
            py::arg("correlation"),
            "Constructs with BS process, Vasicek model, and correlation.");
}
