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
#include <ql/methods/finitedifferences/schemes/douglasscheme.hpp>
#include <ql/methods/finitedifferences/operators/fdmlinearopcomposite.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::douglasscheme(py::module_& m) {
    using bc_set = DouglasScheme::bc_set;
    py::class_<DouglasScheme>(m, "DouglasScheme",
        "Douglas ADI time-stepping scheme.")
        .def(py::init<Real, ext::shared_ptr<FdmLinearOpComposite>,
                       const bc_set&>(),
            py::arg("theta"), py::arg("map"),
            py::arg("bcSet") = bc_set(),
            "Constructs from theta, operator, and boundary conditions.")
        .def("step", [](DouglasScheme& self, Array a, Time t) {
            self.step(a, t);
            return a;
        }, py::arg("a"), py::arg("t"),
            "Applies one time step and returns the modified array.")
        .def("setStep", &DouglasScheme::setStep,
            py::arg("dt"),
            "Sets the time step size.");
}
