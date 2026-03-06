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
#include <ql/methods/finitedifferences/solvers/fdmbatessolver.hpp>
#include <ql/processes/batesprocess.hpp>
#include <ql/methods/finitedifferences/utilities/fdmquantohelper.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmbatessolver(py::module_& m) {
    py::class_<FdmBatesSolver,
               ext::shared_ptr<FdmBatesSolver>,
               LazyObject>(
        m, "FdmBatesSolver",
        "Specialized 2D FDM solver for Bates jump-diffusion model.")
        .def(py::init([](const ext::shared_ptr<BatesProcess>& process,
                         FdmSolverDesc solverDesc,
                         const FdmSchemeDesc& schemeDesc,
                         Size integroIntegrationOrder,
                         const py::object& quantoHelper) {
            Handle<FdmQuantoHelper> qh;
            if (!quantoHelper.is_none())
                qh = quantoHelper.cast<Handle<FdmQuantoHelper>>();
            return ext::make_shared<FdmBatesSolver>(
                Handle<BatesProcess>(process),
                std::move(solverDesc), schemeDesc,
                integroIntegrationOrder, qh);
        }),
            py::arg("process"),
            py::arg("solverDesc"),
            py::arg("schemeDesc") = FdmSchemeDesc::Hundsdorfer(),
            py::arg("integroIntegrationOrder") = 12,
            py::arg("quantoHelper") = py::none(),
            "Constructs from Bates process handle.")
        .def("valueAt", &FdmBatesSolver::valueAt,
            py::arg("s"), py::arg("v"),
            "Returns option value at spot s and variance v.")
        .def("thetaAt", &FdmBatesSolver::thetaAt,
            py::arg("s"), py::arg("v"),
            "Returns theta at spot s and variance v.")
        .def("deltaAt", &FdmBatesSolver::deltaAt,
            py::arg("s"), py::arg("v"),
            "Returns delta at spot s and variance v.")
        .def("gammaAt", &FdmBatesSolver::gammaAt,
            py::arg("s"), py::arg("v"),
            "Returns gamma at spot s and variance v.");
}
