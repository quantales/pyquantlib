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
#include <ql/experimental/variancegamma/analyticvariancegammaengine.hpp>
#include <ql/experimental/variancegamma/variancegammaprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_experimental::analyticvariancegammaengine(py::module_& m) {
    py::class_<VarianceGammaEngine, PricingEngine,
               ext::shared_ptr<VarianceGammaEngine>>(
        m, "VarianceGammaEngine",
        "Analytic Variance Gamma option engine.")
        .def(py::init<ext::shared_ptr<VarianceGammaProcess>, Real>(),
             py::arg("process"),
             py::arg("absoluteError") = 1e-5);
}
