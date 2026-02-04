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
#include <ql/math/interpolation.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::interpolation(py::module_& m) {
    py::class_<Interpolation, Extrapolator, ext::shared_ptr<Interpolation>>(
        m, "Interpolation",
        "Base class for 1-D interpolations.")
        .def("__call__", &Interpolation::operator(),
            py::arg("x"),
            py::arg("allowExtrapolation") = false,
            "Returns interpolated value at x.")
        .def("primitive", &Interpolation::primitive,
            py::arg("x"),
            py::arg("allowExtrapolation") = false,
            "Returns primitive (integral) at x.")
        .def("derivative", &Interpolation::derivative,
            py::arg("x"),
            py::arg("allowExtrapolation") = false,
            "Returns first derivative at x.")
        .def("secondDerivative", &Interpolation::secondDerivative,
            py::arg("x"),
            py::arg("allowExtrapolation") = false,
            "Returns second derivative at x.")
        .def("xMin", &Interpolation::xMin,
            "Returns minimum x value.")
        .def("xMax", &Interpolation::xMax,
            "Returns maximum x value.")
        .def("isInRange", &Interpolation::isInRange,
            py::arg("x"),
            "Returns true if x is in the interpolation range.")
        .def("update", &Interpolation::update,
            "Updates the interpolation after data changes.")
        .def("empty", &Interpolation::empty,
            "Returns true if interpolation is not initialized.");
}
