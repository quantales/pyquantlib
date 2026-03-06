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
#include <ql/methods/finitedifferences/solvers/fdm2dblackscholessolver.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdm2dblackscholessolver(py::module_& m) {
    py::class_<Fdm2dBlackScholesSolver,
               ext::shared_ptr<Fdm2dBlackScholesSolver>,
               LazyObject>(
        m, "Fdm2dBlackScholesSolver",
        "Specialized 2D FDM solver for two-asset Black-Scholes.")
        // Handle-based constructor
        .def(py::init([](const Handle<GeneralizedBlackScholesProcess>& p1,
                         const Handle<GeneralizedBlackScholesProcess>& p2,
                         Real correlation,
                         FdmSolverDesc solverDesc,
                         const FdmSchemeDesc& schemeDesc,
                         bool localVol,
                         const py::object& illegalLocalVolOverwrite) {
            Real overwrite = -Null<Real>();
            if (!illegalLocalVolOverwrite.is_none())
                overwrite = illegalLocalVolOverwrite.cast<Real>();
            return ext::make_shared<Fdm2dBlackScholesSolver>(
                p1, p2, correlation, std::move(solverDesc), schemeDesc,
                localVol, overwrite);
        }),
            py::arg("p1"), py::arg("p2"),
            py::arg("correlation"),
            py::arg("solverDesc"),
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            py::arg("localVol") = false,
            py::arg("illegalLocalVolOverwrite") = py::none(),
            "Constructs from two BS process handles and correlation.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<GeneralizedBlackScholesProcess>& p1,
                         const ext::shared_ptr<GeneralizedBlackScholesProcess>& p2,
                         Real correlation,
                         FdmSolverDesc solverDesc,
                         const FdmSchemeDesc& schemeDesc,
                         bool localVol,
                         const py::object& illegalLocalVolOverwrite) {
            Real overwrite = -Null<Real>();
            if (!illegalLocalVolOverwrite.is_none())
                overwrite = illegalLocalVolOverwrite.cast<Real>();
            return ext::make_shared<Fdm2dBlackScholesSolver>(
                Handle<GeneralizedBlackScholesProcess>(p1),
                Handle<GeneralizedBlackScholesProcess>(p2),
                correlation, std::move(solverDesc), schemeDesc,
                localVol, overwrite);
        }),
            py::arg("p1"), py::arg("p2"),
            py::arg("correlation"),
            py::arg("solverDesc"),
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            py::arg("localVol") = false,
            py::arg("illegalLocalVolOverwrite") = py::none(),
            "Constructs from two BS processes (handles created internally).")
        .def("valueAt", &Fdm2dBlackScholesSolver::valueAt,
            py::arg("x"), py::arg("y"),
            "Returns option value at spot prices x and y.")
        .def("thetaAt", &Fdm2dBlackScholesSolver::thetaAt,
            py::arg("x"), py::arg("y"),
            "Returns theta.")
        .def("deltaXat", &Fdm2dBlackScholesSolver::deltaXat,
            py::arg("x"), py::arg("y"),
            "Returns delta with respect to first asset.")
        .def("deltaYat", &Fdm2dBlackScholesSolver::deltaYat,
            py::arg("x"), py::arg("y"),
            "Returns delta with respect to second asset.")
        .def("gammaXat", &Fdm2dBlackScholesSolver::gammaXat,
            py::arg("x"), py::arg("y"),
            "Returns gamma with respect to first asset.")
        .def("gammaYat", &Fdm2dBlackScholesSolver::gammaYat,
            py::arg("x"), py::arg("y"),
            "Returns gamma with respect to second asset.")
        .def("gammaXYat", &Fdm2dBlackScholesSolver::gammaXYat,
            py::arg("x"), py::arg("y"),
            "Returns cross-gamma between assets.");
}
