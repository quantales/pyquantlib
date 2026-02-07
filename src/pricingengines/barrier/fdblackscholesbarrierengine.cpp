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
#include <ql/pricingengines/barrier/fdblackscholesbarrierengine.hpp>
#include <ql/processes/blackscholesprocess.hpp>
#include <ql/methods/finitedifferences/solvers/fdmbackwardsolver.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::fdblackscholesbarrierengine(py::module_& m) {
    py::class_<FdBlackScholesBarrierEngine, PricingEngine,
               ext::shared_ptr<FdBlackScholesBarrierEngine>>(
        m, "FdBlackScholesBarrierEngine",
        "Finite-differences Black-Scholes barrier option engine.")
        .def(py::init<ext::shared_ptr<GeneralizedBlackScholesProcess>,
                       Size, Size, Size, const FdmSchemeDesc&, bool, Real>(),
            py::arg("process"),
            py::arg("tGrid") = 100,
            py::arg("xGrid") = 100,
            py::arg("dampingSteps") = 0,
            py::arg("schemeDesc") = FdmSchemeDesc::Douglas(),
            py::arg("localVol") = false,
            py::arg("illegalLocalVolOverwrite") = -Null<Real>(),
            "Constructs FdBlackScholesBarrierEngine.");
}
