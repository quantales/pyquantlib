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
#include <ql/processes/geometricbrownianprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::geometricbrownianmotionprocess(py::module_& m) {
    py::class_<GeometricBrownianMotionProcess, StochasticProcess1D,
               ext::shared_ptr<GeometricBrownianMotionProcess>>(
        m, "GeometricBrownianMotionProcess",
        "Geometric Brownian motion process: dS = mu*S*dt + sigma*S*dW.")
        .def(py::init<Real, Real, Real>(),
            py::arg("initialValue"),
            py::arg("mu"),
            py::arg("sigma"),
            "Constructs a GBM process.")
        .def("x0", &GeometricBrownianMotionProcess::x0,
            "Returns initial value.");
}
