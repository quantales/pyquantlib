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
#include <ql/methods/finitedifferences/operators/ninepointlinearop.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::ninepointlinearop(py::module_& m) {
    py::class_<NinePointLinearOp, FdmLinearOp,
               ext::shared_ptr<NinePointLinearOp>>(
        m, "NinePointLinearOp",
        "Nine-point linear operator for 2D FDM grids.")
        .def(py::init<Size, Size, const ext::shared_ptr<FdmMesher>&>(),
            py::arg("d0"), py::arg("d1"), py::arg("mesher"),
            "Constructs from two directions and a mesher.")
        .def("apply", &NinePointLinearOp::apply,
            py::arg("r"),
            "Applies the operator to an array.")
        .def("mult", &NinePointLinearOp::mult,
            py::arg("u"),
            "Left-multiplies by a diagonal matrix.");
}
