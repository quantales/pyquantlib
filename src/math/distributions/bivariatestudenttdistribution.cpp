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
#include <ql/math/distributions/bivariatestudenttdistribution.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::bivariatestudenttdistribution(py::module_& m) {
    py::class_<BivariateCumulativeStudentDistribution>(
        m, "BivariateCumulativeStudentDistribution",
        "Bivariate cumulative Student t distribution function.")
        .def(py::init<Natural, Real>(),
            py::arg("n"), py::arg("rho"),
            "Constructs from the degrees of freedom and correlation.")
        .def("__call__", &BivariateCumulativeStudentDistribution::operator(),
            py::arg("x"), py::arg("y"),
            "Returns the joint cumulative probability at (x, y).");
}
