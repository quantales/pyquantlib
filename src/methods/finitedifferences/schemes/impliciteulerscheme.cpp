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
#include <ql/methods/finitedifferences/schemes/impliciteulerscheme.hpp>
#include <ql/methods/finitedifferences/operators/fdmlinearopcomposite.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::impliciteulerscheme(py::module_& m) {
    using bc_set = ImplicitEulerScheme::bc_set;

    py::enum_<ImplicitEulerScheme::SolverType>(
        m, "ImplicitEulerSolverType",
        "Iterative solver type for implicit schemes.")
        .value("BiCGstab", ImplicitEulerScheme::BiCGstab)
        .value("GMRES", ImplicitEulerScheme::GMRES);

    py::class_<ImplicitEulerScheme>(m, "ImplicitEulerScheme",
        "Implicit Euler time-stepping scheme.")
        .def(py::init<ext::shared_ptr<FdmLinearOpComposite>,
                       const bc_set&, Real,
                       ImplicitEulerScheme::SolverType>(),
            py::arg("map"), py::arg("bcSet") = bc_set(),
            py::arg("relTol") = 1e-8,
            py::arg("solverType") = ImplicitEulerScheme::BiCGstab,
            "Constructs from operator, boundary conditions, and solver settings.")
        .def("step", [](ImplicitEulerScheme& self, Array a, Time t) {
            self.step(a, t);
            return a;
        }, py::arg("a"), py::arg("t"),
            "Applies one time step and returns the modified array.")
        .def("setStep", &ImplicitEulerScheme::setStep,
            py::arg("dt"),
            "Sets the time step size.")
        .def("numberOfIterations", &ImplicitEulerScheme::numberOfIterations,
            "Returns the number of solver iterations in the last step.");
}
