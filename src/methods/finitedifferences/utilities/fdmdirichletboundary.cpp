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
#include <ql/methods/finitedifferences/utilities/fdmdirichletboundary.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

using FdmBoundaryCondition = BoundaryCondition<FdmLinearOp>;

void ql_methods::fdmdirichletboundary(py::module_& m) {
    py::class_<FdmDirichletBoundary,
               ext::shared_ptr<FdmDirichletBoundary>,
               FdmBoundaryCondition>(
        m, "FdmDirichletBoundary",
        "Dirichlet boundary condition for FDM. Sets a fixed value on a boundary.")
        .def(py::init<ext::shared_ptr<FdmMesher>, Real, Size,
                       FdmBoundaryCondition::Side>(),
            py::arg("mesher"), py::arg("valueOnBoundary"),
            py::arg("direction"), py::arg("side"),
            "Constructs with mesher, boundary value, direction, and side.");
}
