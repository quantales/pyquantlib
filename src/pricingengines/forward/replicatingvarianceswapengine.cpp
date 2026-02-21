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
#include <ql/pricingengines/forward/replicatingvarianceswapengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::replicatingvarianceswapengine(py::module_& m) {
    py::class_<ReplicatingVarianceSwapEngine, PricingEngine,
               ext::shared_ptr<ReplicatingVarianceSwapEngine>>(
        m, "ReplicatingVarianceSwapEngine",
        "Variance swap engine using replicating portfolio.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                      Real, const std::vector<Real>&, const std::vector<Real>&>(),
            py::arg("process"),
            py::arg("dk") = 5.0,
            py::arg("callStrikes") = std::vector<Real>(),
            py::arg("putStrikes") = std::vector<Real>(),
            "Constructs the replicating variance swap engine.");
}
