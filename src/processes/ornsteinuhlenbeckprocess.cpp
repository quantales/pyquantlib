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
#include <ql/processes/ornsteinuhlenbeckprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::ornsteinuhlenbeckprocess(py::module_& m) {
    py::class_<OrnsteinUhlenbeckProcess, StochasticProcess1D,
               ext::shared_ptr<OrnsteinUhlenbeckProcess>>(
        m, "OrnsteinUhlenbeckProcess",
        "Ornstein-Uhlenbeck mean-reverting process: "
        "dx = a(r - x)dt + sigma dW.")
        .def(py::init<Real, Volatility, Real, Real>(),
            py::arg("speed"),
            py::arg("volatility"),
            py::arg("x0") = 0.0,
            py::arg("level") = 0.0,
            "Constructs an OU process.")
        .def("x0", &OrnsteinUhlenbeckProcess::x0,
            "Returns initial value.")
        .def("speed", &OrnsteinUhlenbeckProcess::speed,
            "Returns mean reversion speed.")
        .def("volatility", &OrnsteinUhlenbeckProcess::volatility,
            "Returns volatility.")
        .def("level", &OrnsteinUhlenbeckProcess::level,
            "Returns long-term mean level.");
}
