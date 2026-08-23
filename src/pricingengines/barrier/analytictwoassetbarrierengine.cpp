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
#include <ql/pricingengines/barrier/analytictwoassetbarrierengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analytictwoassetbarrierengine(py::module_& m) {
    py::class_<AnalyticTwoAssetBarrierEngine, PricingEngine,
               ext::shared_ptr<AnalyticTwoAssetBarrierEngine>>(
        m, "AnalyticTwoAssetBarrierEngine",
        "Analytic two-asset barrier option engine.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Handle<Quote>>(),
            py::arg("process1"),
            py::arg("process2"),
            py::arg("rho"),
            "Constructs engine with two processes and correlation.")
        .def(py::init([](const ext::shared_ptr<GeneralizedBlackScholesProcess>& p1,
                         const ext::shared_ptr<GeneralizedBlackScholesProcess>& p2,
                         const ext::shared_ptr<Quote>& rho) {
            return ext::make_shared<AnalyticTwoAssetBarrierEngine>(
                p1, p2, Handle<Quote>(rho));
        }),
            py::arg("process1"),
            py::arg("process2"),
            py::arg("rho"),
            "Constructs engine (handle created internally).");
}
