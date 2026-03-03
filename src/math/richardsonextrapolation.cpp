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
#include <ql/math/richardsonextrapolation.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::richardsonextrapolation(py::module_& m) {
    using RE = RichardsonExtrapolation;

    py::class_<RE>(m, "RichardsonExtrapolation",
        "Richardson extrapolation for improving convergence.")
        .def(py::init([](const std::function<Real(Real)>& f, Real delta_h,
                         const py::object& n) {
            Real nVal = n.is_none() ? Null<Real>() : n.cast<Real>();
            return RE(f, delta_h, nVal);
        }),
        py::arg("f"), py::arg("deltaH"), py::arg("n") = py::none(),
        "Constructs from function f, step size delta_h, and optional order n.")
        .def("__call__", static_cast<Real (RE::*)(Real) const>(&RE::operator()),
            py::arg("t") = 2.0,
            "Returns the extrapolated value with ratio t.")
        .def("__call__",
            static_cast<Real (RE::*)(Real, Real) const>(&RE::operator()),
            py::arg("t"), py::arg("s"),
            "Returns the second-order extrapolated value with ratios t and s.");
}
