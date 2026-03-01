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
#include <ql/methods/finitedifferences/solvers/fdmbackwardsolver.hpp>
#include <ql/methods/finitedifferences/stepconditions/fdmstepconditioncomposite.hpp>
#include <ql/methods/finitedifferences/operators/fdmlinearopcomposite.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmbackwardsolver(py::module_& m) {
    // FdmSchemeType enum
    py::enum_<FdmSchemeDesc::FdmSchemeType>(m, "FdmSchemeType",
        "Finite difference scheme types.")
        .value("Hundsdorfer", FdmSchemeDesc::HundsdorferType)
        .value("Douglas", FdmSchemeDesc::DouglasType)
        .value("CraigSneyd", FdmSchemeDesc::CraigSneydType)
        .value("ModifiedCraigSneyd", FdmSchemeDesc::ModifiedCraigSneydType)
        .value("ImplicitEuler", FdmSchemeDesc::ImplicitEulerType)
        .value("ExplicitEuler", FdmSchemeDesc::ExplicitEulerType)
        .value("MethodOfLines", FdmSchemeDesc::MethodOfLinesType)
        .value("TrBDF2", FdmSchemeDesc::TrBDF2Type)
        .value("CrankNicolson", FdmSchemeDesc::CrankNicolsonType)
        .export_values();

    // Struct
    py::class_<FdmSchemeDesc>(m, "FdmSchemeDesc",
        "Finite difference scheme descriptor.")
        .def(py::init<FdmSchemeDesc::FdmSchemeType, Real, Real>(),
            py::arg("type"), py::arg("theta"), py::arg("mu"),
            "Constructs with scheme type, theta, and mu.")
        .def_readonly("type", &FdmSchemeDesc::type)
        .def_readonly("theta", &FdmSchemeDesc::theta)
        .def_readonly("mu", &FdmSchemeDesc::mu)
        // Static factory methods
        .def_static("Douglas", &FdmSchemeDesc::Douglas,
            "Douglas scheme (same as Crank-Nicolson in 1D).")
        .def_static("CrankNicolson", &FdmSchemeDesc::CrankNicolson,
            "Crank-Nicolson scheme.")
        .def_static("ImplicitEuler", &FdmSchemeDesc::ImplicitEuler,
            "Implicit Euler scheme.")
        .def_static("ExplicitEuler", &FdmSchemeDesc::ExplicitEuler,
            "Explicit Euler scheme.")
        .def_static("CraigSneyd", &FdmSchemeDesc::CraigSneyd,
            "Craig-Sneyd scheme.")
        .def_static("ModifiedCraigSneyd", &FdmSchemeDesc::ModifiedCraigSneyd,
            "Modified Craig-Sneyd scheme.")
        .def_static("Hundsdorfer", &FdmSchemeDesc::Hundsdorfer,
            "Hundsdorfer scheme.")
        .def_static("ModifiedHundsdorfer", &FdmSchemeDesc::ModifiedHundsdorfer,
            "Modified Hundsdorfer scheme.")
        .def_static("MethodOfLines", &FdmSchemeDesc::MethodOfLines,
            py::arg("eps") = 0.001, py::arg("relInitStepSize") = 0.01,
            "Method of lines scheme.")
        .def_static("TrBDF2", &FdmSchemeDesc::TrBDF2,
            "TR-BDF2 scheme.");

    // FdmBackwardSolver class
    using bc_set = FdmBoundaryConditionSet;

    py::class_<FdmBackwardSolver>(m, "FdmBackwardSolver",
        "Core FDM backward solver performing PDE rollback.")
        .def(py::init([](ext::shared_ptr<FdmLinearOpComposite> map,
                         bc_set bcSet,
                         const py::object& condition,
                         const FdmSchemeDesc& schemeDesc) {
            ext::shared_ptr<FdmStepConditionComposite> cond;
            if (!condition.is_none())
                cond = condition.cast<ext::shared_ptr<FdmStepConditionComposite>>();
            return FdmBackwardSolver(std::move(map), std::move(bcSet),
                                     cond, schemeDesc);
        }),
            py::arg("map"),
            py::arg("bcSet") = bc_set(),
            py::arg("condition") = py::none(),
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            "Constructs with operator, boundary conditions, step conditions, and scheme.")
        .def("rollback", [](FdmBackwardSolver& self,
                            Array a, Time from, Time to,
                            Size steps, Size dampingSteps) {
            self.rollback(a, from, to, steps, dampingSteps);
            return a;
        },
            py::arg("a"), py::arg("from_"), py::arg("to"),
            py::arg("steps"), py::arg("dampingSteps"),
            "Rolls back array from time 'from' to time 'to' (returns modified copy).");
}
