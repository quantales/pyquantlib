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
#include <ql/termstructures/multicurve.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::multicurve(py::module_& m) {
    py::class_<MultiCurve, Observer, ext::shared_ptr<MultiCurve>>(
        m, "MultiCurve",
        "Manages a set of yield curves that form a dependency cycle.")
        // Accuracy constructor
        .def(py::init<Real>(),
            py::arg("accuracy"),
            "Constructs with a target accuracy for the bootstrap.")
        // Optimizer constructor
        .def(py::init<const ext::shared_ptr<OptimizationMethod>&,
                       const ext::shared_ptr<EndCriteria>&>(),
            py::arg("optimizer") = nullptr,
            py::arg("endCriteria") = nullptr,
            "Constructs with an optimization method and end criteria.")
        // addBootstrappedCurve - wraps the rvalue-ref parameter
        .def("addBootstrappedCurve",
            [](MultiCurve& self,
               RelinkableHandle<YieldTermStructure>& internalHandle,
               ext::shared_ptr<YieldTermStructure> curve) {
                return self.addBootstrappedCurve(internalHandle, std::move(curve));
            },
            py::arg("internalHandle"),
            py::arg("curve"),
            "Adds a bootstrapped curve and returns an external handle.")
        // addNonBootstrappedCurve - wraps the rvalue-ref parameter
        .def("addNonBootstrappedCurve",
            [](MultiCurve& self,
               RelinkableHandle<YieldTermStructure>& internalHandle,
               ext::shared_ptr<YieldTermStructure> curve) {
                return self.addNonBootstrappedCurve(internalHandle, std::move(curve));
            },
            py::arg("internalHandle"),
            py::arg("curve"),
            "Adds a non-bootstrapped curve and returns an external handle.");
}
