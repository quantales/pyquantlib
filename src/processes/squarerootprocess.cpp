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
#include <ql/processes/squarerootprocess.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::squarerootprocess(py::module_& m) {
    py::class_<SquareRootProcess, StochasticProcess1D,
               ext::shared_ptr<SquareRootProcess>>(
        m, "SquareRootProcess",
        "Square root (CIR) process: dx = a(b - x)dt + sigma*sqrt(x)*dW.")
        .def(py::init<Real, Real, Volatility, Real>(),
            py::arg("b"),
            py::arg("a"),
            py::arg("sigma"),
            py::arg("x0") = 0.0,
            "Constructs a square root process.")
        .def("x0", &SquareRootProcess::x0,
            "Returns initial value.")
        .def("a", &SquareRootProcess::a,
            "Returns speed of mean reversion.")
        .def("b", &SquareRootProcess::b,
            "Returns long-term mean.")
        .def("sigma", &SquareRootProcess::sigma,
            "Returns volatility.");
}
