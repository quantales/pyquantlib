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
#include <ql/pricingengines/vanilla/analytichestonhullwhiteengine.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <ql/models/shortrate/onefactormodels/hullwhite.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analytichestonhullwhiteengine(py::module_& m) {
    py::class_<AnalyticHestonHullWhiteEngine,
               ext::shared_ptr<AnalyticHestonHullWhiteEngine>,
               AnalyticHestonEngine>(
        m, "AnalyticHestonHullWhiteEngine",
        "Heston engine with Hull-White stochastic interest rates.")
        // Laguerre integration
        .def(py::init<const ext::shared_ptr<HestonModel>&,
                      ext::shared_ptr<HullWhite>, Size>(),
            py::arg("hestonModel"),
            py::arg("hullWhiteModel"),
            py::arg("integrationOrder") = 144,
            "Constructs with Gauss-Laguerre integration.")
        // Adaptive Gauss-Lobatto
        .def(py::init<const ext::shared_ptr<HestonModel>&,
                      ext::shared_ptr<HullWhite>, Real, Size>(),
            py::arg("hestonModel"),
            py::arg("hullWhiteModel"),
            py::arg("relTolerance"),
            py::arg("maxEvaluations"),
            "Constructs with adaptive Gauss-Lobatto integration.");
}
