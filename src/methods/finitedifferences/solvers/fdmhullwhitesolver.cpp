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
#include <ql/methods/finitedifferences/solvers/fdmhullwhitesolver.hpp>
#include <ql/models/shortrate/onefactormodels/hullwhite.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmhullwhitesolver(py::module_& m) {
    py::class_<FdmHullWhiteSolver,
               ext::shared_ptr<FdmHullWhiteSolver>,
               LazyObject>(
        m, "FdmHullWhiteSolver",
        "Specialized 1D FDM solver for Hull-White interest rate model.")
        // Handle-based constructor
        .def(py::init([](const Handle<HullWhite>& model,
                         FdmSolverDesc solverDesc,
                         const FdmSchemeDesc& schemeDesc) {
            return ext::make_shared<FdmHullWhiteSolver>(
                model, std::move(solverDesc), schemeDesc);
        }),
            py::arg("model"),
            py::arg("solverDesc"),
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            "Constructs from Hull-White model handle.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<HullWhite>& model,
                         FdmSolverDesc solverDesc,
                         const FdmSchemeDesc& schemeDesc) {
            return ext::make_shared<FdmHullWhiteSolver>(
                Handle<HullWhite>(model),
                std::move(solverDesc), schemeDesc);
        }),
            py::arg("model"),
            py::arg("solverDesc"),
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            "Constructs from Hull-White model (handle created internally).")
        .def("valueAt", &FdmHullWhiteSolver::valueAt,
            py::arg("r"),
            "Returns option value at interest rate r.");
}
