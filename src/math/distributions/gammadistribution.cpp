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
#include <ql/math/distributions/gammadistribution.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::gammadistribution(py::module_& m) {
    py::class_<GammaFunction>(
        m, "GammaFunction",
        "Gamma function.")
        .def(py::init<>())
        .def("value", &GammaFunction::value,
            py::arg("x"),
            "Returns the gamma function at x.")
        .def("logValue", &GammaFunction::logValue,
            py::arg("x"),
            "Returns the logarithm of the gamma function at x.");

    py::class_<CumulativeGammaDistribution>(
        m, "CumulativeGammaDistribution",
        "Cumulative gamma distribution function.")
        .def(py::init<Real>(),
            py::arg("a"),
            "Constructs from the shape parameter.")
        .def("__call__", &CumulativeGammaDistribution::operator(),
            py::arg("x"),
            "Returns the cumulative probability at x.");
}
