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
#include <ql/methods/finitedifferences/utilities/fdmtimedepdirichletboundary.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>

namespace py = pybind11;
using namespace QuantLib;

using FdmBoundaryCondition = BoundaryCondition<FdmLinearOp>;

void ql_methods::fdmtimedepdirichletboundary(py::module_& m) {
    py::class_<FdmTimeDepDirichletBoundary,
               ext::shared_ptr<FdmTimeDepDirichletBoundary>,
               FdmBoundaryCondition>(
        m, "FdmTimeDepDirichletBoundary",
        "Time-dependent Dirichlet boundary condition for FDM.")
        .def(py::init<ext::shared_ptr<FdmMesher>,
                       std::function<Real(Real)>,
                       Size, FdmBoundaryCondition::Side>(),
            py::arg("mesher"), py::arg("valueOnBoundary"),
            py::arg("direction"), py::arg("side"),
            "Constructs with scalar time-dependent boundary value function.");
}
