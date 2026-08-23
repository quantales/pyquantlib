/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include "pyquantlib/interpolation_helper.h"
#include <ql/math/interpolations/bicubicsplineinterpolation.hpp>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::bicubicsplineinterpolation(py::module_& m) {
    pyquantlib::bind_simple_interpolation2d<BicubicSpline>(
        m, "BicubicSpline",
        "Bicubic spline interpolation on a 2-D grid.")
        .def("derivativeX", &BicubicSpline::derivativeX,
            py::arg("x"), py::arg("y"),
            "Returns the partial derivative with respect to x.")
        .def("derivativeY", &BicubicSpline::derivativeY,
            py::arg("x"), py::arg("y"),
            "Returns the partial derivative with respect to y.")
        .def("secondDerivativeX", &BicubicSpline::secondDerivativeX,
            py::arg("x"), py::arg("y"),
            "Returns the second partial derivative with respect to x.")
        .def("secondDerivativeY", &BicubicSpline::secondDerivativeY,
            py::arg("x"), py::arg("y"),
            "Returns the second partial derivative with respect to y.")
        .def("derivativeXY", &BicubicSpline::derivativeXY,
            py::arg("x"), py::arg("y"),
            "Returns the cross partial derivative.");
}
