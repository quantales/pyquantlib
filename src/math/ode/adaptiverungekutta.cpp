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
#include <ql/math/ode/adaptiverungekutta.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::adaptiverungekutta(py::module_& m) {
    py::class_<AdaptiveRungeKutta<Real>>(
        m, "AdaptiveRungeKutta",
        "Adaptive step-size Runge-Kutta ODE integrator (Cash-Karp method).")
        .def(py::init<Real, Real, Real>(),
            py::arg("eps") = 1.0e-6,
            py::arg("h1") = 1.0e-4,
            py::arg("hmin") = 0.0,
            "Constructs with prescribed error *eps*, initial step *h1*, and "
            "minimum step *hmin*.")
        // N-dimensional ODE: f'(x) = F(x, f(x))
        .def("__call__",
            [](AdaptiveRungeKutta<Real>& self,
               const std::function<std::vector<Real>(Real, const std::vector<Real>&)>& ode,
               const std::vector<Real>& y1, Real x1, Real x2) {
                return self(ode, y1, x1, x2);
            },
            py::arg("ode"), py::arg("y1"), py::arg("x1"), py::arg("x2"),
            "Integrates N-dimensional ODE from x1 to x2 with initial "
            "condition y(x1) = y1.")
        // 1-dimensional ODE: y'(x) = f(x, y)
        .def("solve1d",
            [](AdaptiveRungeKutta<Real>& self,
               const std::function<Real(Real, Real)>& ode,
               Real y1, Real x1, Real x2) {
                return self(ode, y1, x1, x2);
            },
            py::arg("ode"), py::arg("y1"), py::arg("x1"), py::arg("x2"),
            "Integrates 1-dimensional ODE from x1 to x2 with initial "
            "condition y(x1) = y1.");
}
