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
#include <ql/methods/finitedifferences/solvers/fdmhestonsolver.hpp>
#include <ql/processes/hestonprocess.hpp>
#include <ql/methods/finitedifferences/utilities/fdmquantohelper.hpp>
#include <ql/termstructures/volatility/equityfx/localvoltermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmhestonsolver(py::module_& m) {
    py::class_<FdmHestonSolver,
               ext::shared_ptr<FdmHestonSolver>,
               LazyObject>(
        m, "FdmHestonSolver",
        "Specialized 2D FDM solver for Heston stochastic volatility.")
        // Handle-based constructor
        .def(py::init([](const Handle<HestonProcess>& process,
                         FdmSolverDesc solverDesc,
                         const FdmSchemeDesc& schemeDesc,
                         const py::object& quantoHelper,
                         const py::object& leverageFct,
                         Real mixingFactor) {
            Handle<FdmQuantoHelper> qh;
            if (!quantoHelper.is_none())
                qh = quantoHelper.cast<Handle<FdmQuantoHelper>>();
            ext::shared_ptr<LocalVolTermStructure> lv;
            if (!leverageFct.is_none())
                lv = leverageFct.cast<ext::shared_ptr<LocalVolTermStructure>>();
            return ext::make_shared<FdmHestonSolver>(
                process, std::move(solverDesc), schemeDesc, qh, lv, mixingFactor);
        }),
            py::arg("process"),
            py::arg("solverDesc"),
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            py::arg("quantoHelper") = py::none(),
            py::arg("leverageFct") = py::none(),
            py::arg("mixingFactor") = 1.0,
            "Constructs from Heston process handle.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<HestonProcess>& process,
                         FdmSolverDesc solverDesc,
                         const FdmSchemeDesc& schemeDesc,
                         const py::object& quantoHelper,
                         const py::object& leverageFct,
                         Real mixingFactor) {
            Handle<FdmQuantoHelper> qh;
            if (!quantoHelper.is_none())
                qh = quantoHelper.cast<Handle<FdmQuantoHelper>>();
            ext::shared_ptr<LocalVolTermStructure> lv;
            if (!leverageFct.is_none())
                lv = leverageFct.cast<ext::shared_ptr<LocalVolTermStructure>>();
            return ext::make_shared<FdmHestonSolver>(
                Handle<HestonProcess>(process),
                std::move(solverDesc), schemeDesc, qh, lv, mixingFactor);
        }),
            py::arg("process"),
            py::arg("solverDesc"),
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            py::arg("quantoHelper") = py::none(),
            py::arg("leverageFct") = py::none(),
            py::arg("mixingFactor") = 1.0,
            "Constructs from Heston process (handle created internally).")
        .def("valueAt", &FdmHestonSolver::valueAt,
            py::arg("s"), py::arg("v"),
            "Returns option value at spot s and variance v.")
        .def("thetaAt", &FdmHestonSolver::thetaAt,
            py::arg("s"), py::arg("v"),
            "Returns theta at spot s and variance v.")
        .def("deltaAt", &FdmHestonSolver::deltaAt,
            py::arg("s"), py::arg("v"),
            "Returns delta at spot s and variance v.")
        .def("gammaAt", &FdmHestonSolver::gammaAt,
            py::arg("s"), py::arg("v"),
            "Returns gamma at spot s and variance v.")
        .def("meanVarianceDeltaAt", &FdmHestonSolver::meanVarianceDeltaAt,
            py::arg("s"), py::arg("v"),
            "Returns mean-variance adjusted delta.")
        .def("meanVarianceGammaAt", &FdmHestonSolver::meanVarianceGammaAt,
            py::arg("s"), py::arg("v"),
            "Returns mean-variance adjusted gamma.");
}
