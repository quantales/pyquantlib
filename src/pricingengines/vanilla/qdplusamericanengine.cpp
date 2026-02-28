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
#include "pyquantlib/null_utils.h"
#include <ql/pricingengines/vanilla/qdplusamericanengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::qdplusamericanengine(py::module_& m) {
    py::enum_<QdPlusAmericanEngine::SolverType>(
        m, "QdPlusAmericanEngineSolverType",
        "Solver type for QD+ American engine.")
        .value("Brent", QdPlusAmericanEngine::Brent)
        .value("Newton", QdPlusAmericanEngine::Newton)
        .value("Ridder", QdPlusAmericanEngine::Ridder)
        .value("Halley", QdPlusAmericanEngine::Halley)
        .value("SuperHalley", QdPlusAmericanEngine::SuperHalley);

    py::class_<QdPlusAmericanEngine,
               ext::shared_ptr<QdPlusAmericanEngine>,
               PricingEngine>(
        m, "QdPlusAmericanEngine",
        "QD+ American option pricing engine.")
        .def(py::init([](const ext::shared_ptr<GeneralizedBlackScholesProcess>& process,
                         Size interpolationPoints,
                         QdPlusAmericanEngine::SolverType solverType,
                         Real eps,
                         py::object maxIter) {
            return ext::make_shared<QdPlusAmericanEngine>(
                process, interpolationPoints, solverType, eps,
                from_python_with_null<Size>(maxIter));
        }),
            py::arg("process"),
            py::arg("interpolationPoints") = 8,
            py::arg("solverType") = QdPlusAmericanEngine::Halley,
            py::arg("eps") = 1e-6,
            py::arg("maxIter") = py::none(),
            "Constructs QD+ American engine.");
}
