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
#include <ql/pricingengines/vanilla/analyticcevengine.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::analyticcevengine(py::module_& m) {
    py::class_<CEVCalculator, ext::shared_ptr<CEVCalculator>>(
        m, "CEVCalculator",
        "Constant Elasticity of Variance option value calculator.")
        .def(py::init<Real, Real, Real>(),
            py::arg("f0"),
            py::arg("alpha"),
            py::arg("beta"),
            "Constructs CEVCalculator.")
        .def("value", &CEVCalculator::value,
            py::arg("optionType"), py::arg("strike"), py::arg("t"),
            "Returns CEV option value.")
        .def("f0", &CEVCalculator::f0, "Returns initial forward.")
        .def("alpha", &CEVCalculator::alpha, "Returns alpha.")
        .def("beta", &CEVCalculator::beta, "Returns beta.");

    py::class_<AnalyticCEVEngine, PricingEngine,
               ext::shared_ptr<AnalyticCEVEngine>>(
        m, "AnalyticCEVEngine",
        "Analytic Constant Elasticity of Variance pricing engine.")
        .def(py::init<Real, Real, Real, Handle<YieldTermStructure>>(),
            py::arg("f0"),
            py::arg("alpha"),
            py::arg("beta"),
            py::arg("discountCurve"),
            "Constructs AnalyticCEVEngine.")
        // Hidden handle constructor
        .def(py::init([](Real f0, Real alpha, Real beta,
                         const ext::shared_ptr<YieldTermStructure>& yts) {
                return ext::make_shared<AnalyticCEVEngine>(
                    f0, alpha, beta, Handle<YieldTermStructure>(yts));
             }),
            py::arg("f0"),
            py::arg("alpha"),
            py::arg("beta"),
            py::arg("discountCurve"),
            "Constructs from yield term structure (handle created internally).");
}
