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
#include <ql/experimental/processes/extendedornsteinuhlenbeckprocess.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_processes::extendedornsteinuhlenbeckprocess(py::module_& m) {
    using EOUP = ExtendedOrnsteinUhlenbeckProcess;

    py::enum_<EOUP::Discretization>(
        m, "ExtendedOUDiscretization",
        "Discretization method for ExtendedOrnsteinUhlenbeckProcess.")
        .value("MidPoint", EOUP::MidPoint)
        .value("Trapezodial", EOUP::Trapezodial)
        .value("GaussLobatto", EOUP::GaussLobatto);

    py::class_<EOUP, StochasticProcess1D,
               ext::shared_ptr<EOUP>>(
        m, "ExtendedOrnsteinUhlenbeckProcess",
        "Extended OU process with time-dependent level: "
        "dx = a(b(t) - x)dt + sigma*dW.")
        .def(py::init<Real, Volatility, Real,
                       std::function<Real(Real)>,
                       EOUP::Discretization, Real>(),
            py::arg("speed"),
            py::arg("sigma"),
            py::arg("x0"),
            py::arg("b"),
            py::arg("discretization") = EOUP::MidPoint,
            py::arg("intEps") = 1e-4,
            "Constructs with time-dependent level function b(t).")
        .def("x0", &EOUP::x0,
            "Returns initial value.")
        .def("speed", &EOUP::speed,
            "Returns mean reversion speed.")
        .def("volatility", &EOUP::volatility,
            "Returns volatility.");
}
