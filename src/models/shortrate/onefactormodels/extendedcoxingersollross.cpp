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
#include <ql/models/shortrate/onefactormodels/extendedcoxingersollross.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_models::extendedcoxingersollross(py::module_& m) {
    py::class_<ExtendedCoxIngersollRoss, CoxIngersollRoss,
               TermStructureConsistentModel,
               ext::shared_ptr<ExtendedCoxIngersollRoss>>(
        m, "ExtendedCoxIngersollRoss",
        "Extended Cox-Ingersoll-Ross model fitted to term structure.")
        .def(py::init<const Handle<YieldTermStructure>&,
                      Real, Real, Real, Real, bool>(),
            py::arg("termStructure"),
            py::arg("theta") = 0.1,
            py::arg("k") = 0.1,
            py::arg("sigma") = 0.1,
            py::arg("x0") = 0.05,
            py::arg("withFellerConstraint") = true,
            "Constructs extended CIR model.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& ts,
                         Real theta, Real k, Real sigma, Real x0,
                         bool withFellerConstraint) {
            return ext::make_shared<ExtendedCoxIngersollRoss>(
                Handle<YieldTermStructure>(ts),
                theta, k, sigma, x0, withFellerConstraint);
        }),
            py::arg("termStructure"),
            py::arg("theta") = 0.1,
            py::arg("k") = 0.1,
            py::arg("sigma") = 0.1,
            py::arg("x0") = 0.05,
            py::arg("withFellerConstraint") = true,
            "Constructs extended CIR model (handle created internally).");
}
