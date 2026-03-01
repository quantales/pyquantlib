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
#include <ql/methods/finitedifferences/solvers/fdmsolverdesc.hpp>
#include <ql/methods/finitedifferences/stepconditions/fdmstepconditioncomposite.hpp>
#include <ql/methods/finitedifferences/utilities/fdminnervaluecalculator.hpp>
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmsolverdesc(py::module_& m) {
    using bc_set = FdmBoundaryConditionSet;

    py::class_<FdmSolverDesc>(m, "FdmSolverDesc",
        "Descriptor for FDM solver configuration.")
        .def(py::init([](const ext::shared_ptr<FdmMesher>& mesher,
                         const bc_set& bcSet,
                         const ext::shared_ptr<FdmStepConditionComposite>& condition,
                         const ext::shared_ptr<FdmInnerValueCalculator>& calculator,
                         Time maturity,
                         Size timeSteps,
                         Size dampingSteps) {
            return FdmSolverDesc{mesher, bcSet, condition, calculator,
                                 maturity, timeSteps, dampingSteps};
        }),
            py::arg("mesher"),
            py::arg("bcSet"),
            py::arg("condition"),
            py::arg("calculator"),
            py::arg("maturity"),
            py::arg("timeSteps"),
            py::arg("dampingSteps") = Size(0),
            "Constructs solver descriptor.")
        .def_readonly("mesher", &FdmSolverDesc::mesher)
        .def_readonly("bcSet", &FdmSolverDesc::bcSet)
        .def_readonly("condition", &FdmSolverDesc::condition)
        .def_readonly("calculator", &FdmSolverDesc::calculator)
        .def_readonly("maturity", &FdmSolverDesc::maturity)
        .def_readonly("timeSteps", &FdmSolverDesc::timeSteps)
        .def_readonly("dampingSteps", &FdmSolverDesc::dampingSteps);
}
