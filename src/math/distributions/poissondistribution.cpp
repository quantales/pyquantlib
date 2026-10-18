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
#include <ql/math/distributions/poissondistribution.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::poissondistribution(py::module_& m) {
    py::class_<PoissonDistribution>(
        m, "PoissonDistribution",
        "Poisson probability mass function.")
        .def(py::init<Real>(),
            py::arg("mu"),
            "Constructs from the mean.")
        .def("__call__", &PoissonDistribution::operator(),
            py::arg("k"),
            "Returns the probability of k events.");

    py::class_<CumulativePoissonDistribution>(
        m, "CumulativePoissonDistribution",
        "Cumulative Poisson distribution function.")
        .def(py::init<Real>(),
            py::arg("mu"),
            "Constructs from the mean.")
        .def("__call__", &CumulativePoissonDistribution::operator(),
            py::arg("k"),
            "Returns the probability of at most k events.");

    py::class_<InverseCumulativePoisson>(
        m, "InverseCumulativePoisson",
        "Inverse cumulative Poisson distribution function.")
        // The shorter overload lets QuantLib supply the default mean.
        .def(py::init<>(),
            "Constructs with QuantLib's default mean.")
        .def(py::init<Real>(),
            py::arg("mu"),
            "Constructs from the mean.")
        .def("__call__", &InverseCumulativePoisson::operator(),
            py::arg("x"),
            "Returns the smallest k whose cumulative probability reaches x.");
}
