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
#include <ql/math/distributions/studenttdistribution.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::studenttdistribution(py::module_& m) {
    py::class_<StudentDistribution>(
        m, "StudentDistribution",
        "Student t probability density function.")
        .def(py::init<Integer>(),
            py::arg("n"),
            "Constructs from the degrees of freedom.")
        .def("__call__", &StudentDistribution::operator(),
            py::arg("x"),
            "Returns the probability density at x.");

    py::class_<CumulativeStudentDistribution>(
        m, "CumulativeStudentDistribution",
        "Cumulative Student t distribution function.")
        .def(py::init<Integer>(),
            py::arg("n"),
            "Constructs from the degrees of freedom.")
        .def("__call__", &CumulativeStudentDistribution::operator(),
            py::arg("x"),
            "Returns the cumulative probability at x.");

    py::class_<InverseCumulativeStudent>(
        m, "InverseCumulativeStudent",
        "Inverse cumulative Student t distribution function.")
        .def(py::init<Integer>(),
            py::arg("n"),
            "Constructs from the degrees of freedom.")
        .def("__call__", &InverseCumulativeStudent::operator(),
            py::arg("x"),
            "Returns the quantile at probability x.");
}
