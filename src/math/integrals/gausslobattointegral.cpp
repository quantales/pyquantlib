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
#include <ql/math/integrals/gausslobattointegral.hpp>
#include <ql/utilities/null.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::gausslobattointegral(py::module_& m) {
    py::class_<GaussLobattoIntegral, Integrator,
               ext::shared_ptr<GaussLobattoIntegral>>(
        m, "GaussLobattoIntegral",
        "Adaptive Gauss-Lobatto integration.")
        .def(py::init([](Size maxIterations, Real absAccuracy,
                         const py::object& relAccuracy, bool useConvergenceEstimate) {
            Real relAcc = relAccuracy.is_none()
                ? Null<Real>()
                : relAccuracy.cast<Real>();
            return ext::make_shared<GaussLobattoIntegral>(
                maxIterations, absAccuracy, relAcc, useConvergenceEstimate);
        }),
        py::arg("maxIterations"),
        py::arg("absAccuracy"),
        py::arg("relAccuracy") = py::none(),
        py::arg("useConvergenceEstimate") = true,
        "Constructs with max iterations, absolute accuracy, optional relative accuracy, "
        "and convergence estimate flag.");
}
