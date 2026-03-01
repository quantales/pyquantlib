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
#include <ql/methods/finitedifferences/schemes/methodoflinesscheme.hpp>
#include <ql/methods/finitedifferences/operators/fdmlinearopcomposite.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::methodoflinesscheme(py::module_& m) {
    using bc_set = MethodOfLinesScheme::bc_set;
    py::class_<MethodOfLinesScheme>(m, "MethodOfLinesScheme",
        "Method of lines time-stepping scheme (Runge-Kutta).")
        .def(py::init<Real, Real,
                       ext::shared_ptr<FdmLinearOpComposite>,
                       const bc_set&>(),
            py::arg("eps"), py::arg("relInitStepSize"),
            py::arg("map"), py::arg("bcSet") = bc_set(),
            "Constructs from tolerance, initial step size, operator, and BCs.")
        .def("step", [](MethodOfLinesScheme& self, Array a, Time t) {
            self.step(a, t);
            return a;
        }, py::arg("a"), py::arg("t"),
            "Applies one time step and returns the modified array.")
        .def("setStep", &MethodOfLinesScheme::setStep,
            py::arg("dt"),
            "Sets the time step size.");
}
