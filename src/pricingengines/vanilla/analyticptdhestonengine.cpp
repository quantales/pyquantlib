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
#include <ql/pricingengines/vanilla/analyticptdhestonengine.hpp>
#include <ql/pricingengines/vanilla/analytichestonengine.hpp>
#include <ql/models/equity/piecewisetimedependenthestonmodel.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticptdhestonengine(py::module_& m) {
    using PTDEngine = AnalyticPTDHestonEngine;

    py::class_<PTDEngine,
               ext::shared_ptr<PTDEngine>,
               PricingEngine>(
        m, "AnalyticPTDHestonEngine",
        "Analytic piecewise time-dependent Heston engine.")
        // Adaptive Gauss-Lobatto
        .def(py::init<const ext::shared_ptr<PiecewiseTimeDependentHestonModel>&,
                      Real, Size>(),
            py::arg("model"), py::arg("relTolerance"), py::arg("maxEvaluations"),
            "Constructs with adaptive Gauss-Lobatto integration.")
        // Laguerre integration order
        .def(py::init<const ext::shared_ptr<PiecewiseTimeDependentHestonModel>&,
                      Size>(),
            py::arg("model"), py::arg("integrationOrder") = 144,
            "Constructs with Gauss-Laguerre integration.")
        // Full control
        .def(py::init<const ext::shared_ptr<PiecewiseTimeDependentHestonModel>&,
                      PTDEngine::ComplexLogFormula,
                      const AnalyticHestonEngine::Integration&, Real>(),
            py::arg("model"), py::arg("cpxLog"), py::arg("integration"),
            py::arg("andersenPiterbargEpsilon") = 1e-8,
            "Constructs with full control over integration method.")
        .def("numberOfEvaluations", &PTDEngine::numberOfEvaluations,
            "Returns number of integration evaluations.");
}
