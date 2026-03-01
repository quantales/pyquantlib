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
#include <ql/methods/finitedifferences/operators/fdmlinearopcomposite.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmlinearopcomposite(py::module_& m) {
    py::class_<FdmLinearOpComposite, FdmLinearOp,
               ext::shared_ptr<FdmLinearOpComposite>>(
        m, "FdmLinearOpComposite",
        "Composite linear operator for multi-dimensional FDM problems.")
        .def("size", &FdmLinearOpComposite::size,
            "Returns the number of operator dimensions.")
        .def("setTime", &FdmLinearOpComposite::setTime,
            py::arg("t1"), py::arg("t2"),
            "Sets the time interval.")
        .def("apply_mixed", &FdmLinearOpComposite::apply_mixed,
            py::arg("r"),
            "Applies the mixed derivative part.")
        .def("apply_direction", &FdmLinearOpComposite::apply_direction,
            py::arg("direction"), py::arg("r"),
            "Applies the operator in a single direction.")
        .def("solve_splitting", &FdmLinearOpComposite::solve_splitting,
            py::arg("direction"), py::arg("r"), py::arg("s"),
            "Solves the implicit splitting step.")
        .def("preconditioner", &FdmLinearOpComposite::preconditioner,
            py::arg("r"), py::arg("s"),
            "Applies the preconditioner.");
}
