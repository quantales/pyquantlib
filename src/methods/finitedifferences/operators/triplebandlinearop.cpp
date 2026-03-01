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
#include <ql/methods/finitedifferences/operators/triplebandlinearop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::triplebandlinearop(py::module_& m) {
    py::class_<TripleBandLinearOp, FdmLinearOp,
               ext::shared_ptr<TripleBandLinearOp>>(
        m, "TripleBandLinearOp",
        "Triple-band (tridiagonal) linear operator.")
        .def(py::init<Size, const ext::shared_ptr<FdmMesher>&>(),
            py::arg("direction"), py::arg("mesher"),
            "Constructs from direction and mesher.")
        .def("apply", &TripleBandLinearOp::apply,
            py::arg("r"),
            "Applies the operator to an array.")
        .def("solve_splitting", &TripleBandLinearOp::solve_splitting,
            py::arg("r"), py::arg("a"), py::arg("b") = 1.0,
            "Solves the splitting step.")
        .def("mult", &TripleBandLinearOp::mult,
            py::arg("u"),
            "Left-multiplies by a diagonal matrix.")
        .def("multR", &TripleBandLinearOp::multR,
            py::arg("u"),
            "Right-multiplies by a diagonal matrix.")
        .def("add",
            py::overload_cast<const TripleBandLinearOp&>(
                &TripleBandLinearOp::add, py::const_),
            py::arg("m"),
            "Adds another triple-band operator.")
        .def("add",
            py::overload_cast<const Array&>(
                &TripleBandLinearOp::add, py::const_),
            py::arg("u"),
            "Adds a diagonal array.")
        .def("axpyb", &TripleBandLinearOp::axpyb,
            py::arg("a"), py::arg("x"), py::arg("y"), py::arg("b"),
            "Computes a*x + y + b (in-place).");
}
