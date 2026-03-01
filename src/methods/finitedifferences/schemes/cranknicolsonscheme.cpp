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
#include <ql/methods/finitedifferences/schemes/cranknicolsonscheme.hpp>
#include <ql/methods/finitedifferences/operators/fdmlinearopcomposite.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::cranknicolsonscheme(py::module_& m) {
    using bc_set = CrankNicolsonScheme::bc_set;
    py::class_<CrankNicolsonScheme>(m, "CrankNicolsonScheme",
        "Crank-Nicolson time-stepping scheme.")
        .def(py::init<Real, const ext::shared_ptr<FdmLinearOpComposite>&,
                       const bc_set&, Real,
                       ImplicitEulerScheme::SolverType>(),
            py::arg("theta"),
            py::arg("map"), py::arg("bcSet") = bc_set(),
            py::arg("relTol") = 1e-8,
            py::arg("solverType") = ImplicitEulerScheme::BiCGstab,
            "Constructs from theta, operator, and solver settings.")
        .def("step", [](CrankNicolsonScheme& self, Array a, Time t) {
            self.step(a, t);
            return a;
        }, py::arg("a"), py::arg("t"),
            "Applies one time step and returns the modified array.")
        .def("setStep", &CrankNicolsonScheme::setStep,
            py::arg("dt"),
            "Sets the time step size.")
        .def("numberOfIterations", &CrankNicolsonScheme::numberOfIterations,
            "Returns the number of solver iterations in the last step.");
}
