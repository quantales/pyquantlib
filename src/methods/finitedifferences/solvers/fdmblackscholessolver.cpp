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
#include <ql/methods/finitedifferences/solvers/fdmblackscholessolver.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/methods/finitedifferences/utilities/fdmquantohelper.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmblackscholessolver(py::module_& m) {
    py::class_<FdmBlackScholesSolver,
               ext::shared_ptr<FdmBlackScholesSolver>,
               LazyObject>(
        m, "FdmBlackScholesSolver",
        "Specialized 1D FDM solver for Black-Scholes processes.")
        // Explicit handle constructor
        .def(py::init([](const Handle<GeneralizedBlackScholesProcess>& process,
                         Real strike,
                         FdmSolverDesc solverDesc,
                         const FdmSchemeDesc& schemeDesc,
                         bool localVol,
                         const py::object& illegalLocalVolOverwrite,
                         const py::object& quantoHelper) {
            Real overwrite = -Null<Real>();
            if (!illegalLocalVolOverwrite.is_none())
                overwrite = illegalLocalVolOverwrite.cast<Real>();
            Handle<FdmQuantoHelper> qh;
            if (!quantoHelper.is_none())
                qh = quantoHelper.cast<Handle<FdmQuantoHelper>>();
            return ext::make_shared<FdmBlackScholesSolver>(
                process, strike, std::move(solverDesc), schemeDesc,
                localVol, overwrite, qh);
        }),
            py::arg("process"),
            py::arg("strike"),
            py::arg("solverDesc"),
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            py::arg("localVol") = false,
            py::arg("illegalLocalVolOverwrite") = py::none(),
            py::arg("quantoHelper") = py::none(),
            "Constructs from process handle.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
                         Real strike,
                         FdmSolverDesc solverDesc,
                         const FdmSchemeDesc& schemeDesc,
                         bool localVol,
                         const py::object& illegalLocalVolOverwrite,
                         const py::object& quantoHelper) {
            Real overwrite = -Null<Real>();
            if (!illegalLocalVolOverwrite.is_none())
                overwrite = illegalLocalVolOverwrite.cast<Real>();
            Handle<FdmQuantoHelper> qh;
            if (!quantoHelper.is_none()) {
                auto ptr = quantoHelper.cast<ext::shared_ptr<FdmQuantoHelper>>();
                if (ptr)
                    qh = Handle<FdmQuantoHelper>(ptr);
            }
            return ext::make_shared<FdmBlackScholesSolver>(
                Handle<GeneralizedBlackScholesProcess>(process),
                strike, std::move(solverDesc), schemeDesc,
                localVol, overwrite, qh);
        }),
            py::arg("process"),
            py::arg("strike"),
            py::arg("solverDesc"),
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            py::arg("localVol") = false,
            py::arg("illegalLocalVolOverwrite") = py::none(),
            py::arg("quantoHelper") = py::none(),
            "Constructs from process (handle created internally).")
        .def("valueAt", &FdmBlackScholesSolver::valueAt,
            py::arg("s"),
            "Returns option value at spot price s.")
        .def("deltaAt", &FdmBlackScholesSolver::deltaAt,
            py::arg("s"),
            "Returns delta at spot price s.")
        .def("gammaAt", &FdmBlackScholesSolver::gammaAt,
            py::arg("s"),
            "Returns gamma at spot price s.")
        .def("thetaAt", &FdmBlackScholesSolver::thetaAt,
            py::arg("s"),
            "Returns theta at spot price s.");
}
