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
#include <ql/pricingengines/vanilla/analyticpdfhestonengine.hpp>
#include <ql/models/equity/hestonmodel.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticpdfhestonengine(py::module_& m) {
    py::class_<AnalyticPDFHestonEngine,
               ext::shared_ptr<AnalyticPDFHestonEngine>,
               PricingEngine>(
        m, "AnalyticPDFHestonEngine",
        "PDF-based Heston engine for arbitrary European payoffs.")
        .def(py::init<ext::shared_ptr<HestonModel>, Real, Size>(),
            py::arg("model"),
            py::arg("gaussLobattoEps") = 1e-6,
            py::arg("gaussLobattoIntegrationOrder") = 10000,
            "Constructs PDF Heston engine.")
        .def("Pv", &AnalyticPDFHestonEngine::Pv,
            py::arg("x_t"), py::arg("t"),
            "Returns probability density in log-space.")
        .def("cdf", &AnalyticPDFHestonEngine::cdf,
            py::arg("X"), py::arg("t"),
            "Returns cumulative distribution function Pr(x < X).");
}
