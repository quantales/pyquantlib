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
#include <ql/math/interpolations/interpolation2d.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::interpolation2d(py::module_& m) {
    py::class_<Interpolation2D, Extrapolator,
               ext::shared_ptr<Interpolation2D>>(
        m, "Interpolation2D",
        "Base class for 2-D interpolation.")
        .def("__call__", &Interpolation2D::operator(),
            py::arg("x"), py::arg("y"),
            py::arg("allowExtrapolation") = false,
            "Returns the interpolated value at (x, y).")
        .def("xMin", &Interpolation2D::xMin,
            "Returns the minimum x value.")
        .def("xMax", &Interpolation2D::xMax,
            "Returns the maximum x value.")
        .def("xValues", &Interpolation2D::xValues,
            "Returns the x values.")
        .def("yMin", &Interpolation2D::yMin,
            "Returns the minimum y value.")
        .def("yMax", &Interpolation2D::yMax,
            "Returns the maximum y value.")
        .def("yValues", &Interpolation2D::yValues,
            "Returns the y values.")
        .def("zData", &Interpolation2D::zData,
            py::return_value_policy::reference_internal,
            "Returns the z data matrix.")
        .def("isInRange", &Interpolation2D::isInRange,
            py::arg("x"), py::arg("y"),
            "Returns true if (x, y) is in range.")
        .def("update", &Interpolation2D::update,
            "Recalculates the interpolation.");
}
