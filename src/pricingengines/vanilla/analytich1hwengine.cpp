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
#include <ql/pricingengines/vanilla/analytich1hwengine.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <ql/models/shortrate/onefactormodels/hullwhite.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analytich1hwengine(py::module_& m) {
    py::class_<AnalyticH1HWEngine,
               ext::shared_ptr<AnalyticH1HWEngine>,
               AnalyticHestonHullWhiteEngine>(
        m, "AnalyticH1HWEngine",
        "H1-HW approximation with equity-rate correlation.")
        // Laguerre integration
        .def(py::init<const ext::shared_ptr<HestonModel>&,
                      const ext::shared_ptr<HullWhite>&,
                      Real, Size>(),
            py::arg("model"),
            py::arg("hullWhiteModel"),
            py::arg("rhoSr"),
            py::arg("integrationOrder") = 144,
            "Constructs with Gauss-Laguerre integration.")
        // Adaptive Gauss-Lobatto
        .def(py::init<const ext::shared_ptr<HestonModel>&,
                      const ext::shared_ptr<HullWhite>&,
                      Real, Real, Size>(),
            py::arg("model"),
            py::arg("hullWhiteModel"),
            py::arg("rhoSr"),
            py::arg("relTolerance"),
            py::arg("maxEvaluations"),
            "Constructs with adaptive Gauss-Lobatto integration.");
}
