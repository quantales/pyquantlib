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
#include <ql/pricingengines/exotic/analytictwoassetcorrelationengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analytictwoassetcorrelationengine(py::module_& m) {
    py::class_<AnalyticTwoAssetCorrelationEngine,
               PricingEngine,
               ext::shared_ptr<AnalyticTwoAssetCorrelationEngine>>(
        m, "AnalyticTwoAssetCorrelationEngine",
        "Analytic two-asset correlation option engine.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Handle<Quote>>(),
             py::arg("p1"),
             py::arg("p2"),
             py::arg("correlation"))
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<GeneralizedBlackScholesProcess>& p1,
                         const ext::shared_ptr<GeneralizedBlackScholesProcess>& p2,
                         const ext::shared_ptr<Quote>& correlation) {
                 return ext::make_shared<AnalyticTwoAssetCorrelationEngine>(
                     p1, p2, Handle<Quote>(correlation));
             }),
             py::arg("p1"),
             py::arg("p2"),
             py::arg("correlation"),
             "Constructs from shared_ptr correlation (handle created internally).");
}
