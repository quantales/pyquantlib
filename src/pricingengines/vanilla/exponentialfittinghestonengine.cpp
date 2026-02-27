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
#include "pyquantlib/null_utils.h"
#include <ql/pricingengines/vanilla/exponentialfittinghestonengine.hpp>
#include <ql/pricingengines/vanilla/analytichestonengine.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::exponentialfittinghestonengine(py::module_& m) {
    py::class_<ExponentialFittingHestonEngine,
               ext::shared_ptr<ExponentialFittingHestonEngine>,
               PricingEngine>(
        m, "ExponentialFittingHestonEngine",
        "Heston engine using exponentially-fitted Gauss-Laguerre quadrature.")
        .def(py::init([](const ext::shared_ptr<HestonModel>& model,
                        AnalyticHestonEngine::ComplexLogFormula cv,
                        py::object scaling,
                        Real alpha) {
            Real scalingVal = from_python_with_null<Real>(scaling);
            return ext::make_shared<ExponentialFittingHestonEngine>(
                model, cv, scalingVal, alpha);
        }),
            py::arg("model"),
            py::arg("cv") = AnalyticHestonEngine::OptimalCV,
            py::arg("scaling") = py::none(),
            py::arg("alpha") = -0.5,
            "Constructs exponential fitting Heston engine.");
}
