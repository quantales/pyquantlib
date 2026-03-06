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
#include <ql/processes/g2process.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::g2process(py::module_& m) {
    py::class_<G2Process, StochasticProcess,
               ext::shared_ptr<G2Process>>(
        m, "G2Process",
        "G2 two-factor short-rate stochastic process.")
        .def(py::init<Real, Real, Real, Real, Real>(),
            py::arg("a"), py::arg("sigma"),
            py::arg("b"), py::arg("eta"),
            py::arg("rho"),
            "Constructs G2Process.")
        .def("x0", &G2Process::x0, "Returns initial x value.")
        .def("y0", &G2Process::y0, "Returns initial y value.")
        .def("a", &G2Process::a, "Returns mean reversion speed a.")
        .def("sigma", &G2Process::sigma, "Returns volatility sigma.")
        .def("b", &G2Process::b, "Returns mean reversion speed b.")
        .def("eta", &G2Process::eta, "Returns volatility eta.")
        .def("rho", &G2Process::rho, "Returns correlation rho.");

    py::class_<G2ForwardProcess, ForwardMeasureProcess,
               ext::shared_ptr<G2ForwardProcess>>(
        m, "G2ForwardProcess",
        "G2 forward-measure two-factor short-rate process.")
        .def(py::init<Real, Real, Real, Real, Real>(),
            py::arg("a"), py::arg("sigma"),
            py::arg("b"), py::arg("eta"),
            py::arg("rho"),
            "Constructs G2ForwardProcess.");
}
