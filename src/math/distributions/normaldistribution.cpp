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
#include <ql/math/distributions/normaldistribution.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::normaldistribution(py::module_& m) {
    py::class_<NormalDistribution>(
        m, "NormalDistribution",
        "Normal (Gaussian) distribution function.")
        .def(py::init<Real, Real>(),
            py::arg("average") = 0.0,
            py::arg("sigma") = 1.0,
            "Constructs NormalDistribution.")
        .def("__call__", &NormalDistribution::operator(),
            py::arg("x"),
            "Returns the probability density at x.")
        .def("derivative", &NormalDistribution::derivative,
            py::arg("x"),
            "Returns the derivative of the density at x.");

    py::class_<CumulativeNormalDistribution>(
        m, "CumulativeNormalDistribution",
        "Cumulative normal distribution function.")
        .def(py::init<Real, Real>(),
            py::arg("average") = 0.0,
            py::arg("sigma") = 1.0,
            "Constructs CumulativeNormalDistribution.")
        .def("__call__", &CumulativeNormalDistribution::operator(),
            py::arg("x"),
            "Returns the cumulative probability at x.")
        .def("derivative", &CumulativeNormalDistribution::derivative,
            py::arg("x"),
            "Returns the derivative (density) at x.");

    py::class_<InverseCumulativeNormal>(
        m, "InverseCumulativeNormal",
        "Inverse cumulative normal distribution function.")
        .def(py::init<Real, Real>(),
            py::arg("average") = 0.0,
            py::arg("sigma") = 1.0,
            "Constructs InverseCumulativeNormal.")
        .def("__call__", &InverseCumulativeNormal::operator(),
            py::arg("x"),
            "Returns the inverse cumulative normal at x.")
        .def_static("standard_value", &InverseCumulativeNormal::standard_value,
            py::arg("x"),
            "Returns the inverse for standard normal (average=0, sigma=1).");
}
