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
#include <ql/models/shortrate/onefactormodels/blackkarasinski.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::blackkarasinski(py::module_& m) {
    py::class_<BlackKarasinski, OneFactorModel, TermStructureConsistentModel,
               ext::shared_ptr<BlackKarasinski>>(
        m, "BlackKarasinski",
        "Black-Karasinski model: d(ln r) = (theta(t) - a*ln(r))dt + sigma*dW.")
        // Constructor with handle
        .def(py::init<const Handle<YieldTermStructure>&, Real, Real>(),
            py::arg("termStructure"),
            py::arg("a") = 0.1,
            py::arg("sigma") = 0.1,
            "Constructs Black-Karasinski model with term structure, mean reversion, and volatility.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& ts,
                        Real a, Real sigma) {
            return ext::make_shared<BlackKarasinski>(
                Handle<YieldTermStructure>(ts), a, sigma);
        }),
            py::arg("termStructure"),
            py::arg("a") = 0.1,
            py::arg("sigma") = 0.1,
            "Constructs Black-Karasinski model from term structure.");
}
