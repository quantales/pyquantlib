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
#include <ql/methods/finitedifferences/operators/fdmlinearop.hpp>
#include <ql/methods/finitedifferences/boundarycondition.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

using FdmBoundaryCondition = BoundaryCondition<FdmLinearOp>;

void ql_methods::boundarycondition(py::module_& m) {
    py::class_<FdmBoundaryCondition,
               ext::shared_ptr<FdmBoundaryCondition>>(
        m, "FdmBoundaryCondition",
        "Boundary condition for FDM operators.")
        .def("setTime", &FdmBoundaryCondition::setTime,
            py::arg("t"),
            "Sets the current time for time-dependent conditions.");

    py::enum_<FdmBoundaryCondition::Side>(
        m, "BoundaryConditionSide",
        "Boundary condition side.")
        .value("None_", FdmBoundaryCondition::None)
        .value("Upper", FdmBoundaryCondition::Upper)
        .value("Lower", FdmBoundaryCondition::Lower);
}
