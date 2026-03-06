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
#include <ql/methods/finitedifferences/solvers/fdmg2solver.hpp>
#include <ql/models/shortrate/twofactormodels/g2.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmg2solver(py::module_& m) {
    py::class_<FdmG2Solver,
               ext::shared_ptr<FdmG2Solver>,
               LazyObject>(
        m, "FdmG2Solver",
        "Specialized 2D FDM solver for G2++ two-factor interest rate model.")
        // Handle-based constructor
        .def(py::init([](const Handle<G2>& model,
                         FdmSolverDesc solverDesc,
                         const FdmSchemeDesc& schemeDesc) {
            return ext::make_shared<FdmG2Solver>(
                model, std::move(solverDesc), schemeDesc);
        }),
            py::arg("model"),
            py::arg("solverDesc"),
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            "Constructs from G2 model handle.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<G2>& model,
                         FdmSolverDesc solverDesc,
                         const FdmSchemeDesc& schemeDesc) {
            return ext::make_shared<FdmG2Solver>(
                Handle<G2>(model),
                std::move(solverDesc), schemeDesc);
        }),
            py::arg("model"),
            py::arg("solverDesc"),
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            "Constructs from G2 model (handle created internally).")
        .def("valueAt", &FdmG2Solver::valueAt,
            py::arg("x"), py::arg("y"),
            "Returns option value at state variables x and y.");
}
