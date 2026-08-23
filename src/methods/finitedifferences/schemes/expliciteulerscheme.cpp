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
#include <ql/methods/finitedifferences/schemes/expliciteulerscheme.hpp>
#include <ql/methods/finitedifferences/operators/fdmlinearopcomposite.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::expliciteulerscheme(py::module_& m) {
    using bc_set = ExplicitEulerScheme::bc_set;
    py::class_<ExplicitEulerScheme>(m, "ExplicitEulerScheme",
        "Explicit Euler time-stepping scheme.")
        .def(py::init<ext::shared_ptr<FdmLinearOpComposite>,
                       const bc_set&>(),
            py::arg("map"), py::arg("bcSet") = bc_set(),
            "Constructs from operator and boundary conditions.")
        .def("step", [](ExplicitEulerScheme& self, Array a, Time t) {
            self.step(a, t);
            return a;
        }, py::arg("a"), py::arg("t"),
            "Applies one time step and returns the modified array.")
        .def("setStep", &ExplicitEulerScheme::setStep,
            py::arg("dt"),
            "Sets the time step size.");
}
