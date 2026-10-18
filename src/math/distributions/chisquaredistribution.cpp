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
#include <ql/math/distributions/chisquaredistribution.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::chisquaredistribution(py::module_& m) {
    py::class_<CumulativeChiSquareDistribution>(
        m, "CumulativeChiSquareDistribution",
        "Cumulative chi-square distribution function.")
        .def(py::init<Real>(),
            py::arg("df"),
            "Constructs from the degrees of freedom.")
        .def("__call__", &CumulativeChiSquareDistribution::operator(),
            py::arg("x"),
            "Returns the cumulative probability at x.");

    py::class_<NonCentralCumulativeChiSquareDistribution>(
        m, "NonCentralCumulativeChiSquareDistribution",
        "Cumulative non-central chi-square distribution function.")
        .def(py::init<Real, Real>(),
            py::arg("df"), py::arg("ncp"),
            "Constructs from the degrees of freedom and non-centrality parameter.")
        .def("__call__", &NonCentralCumulativeChiSquareDistribution::operator(),
            py::arg("x"),
            "Returns the cumulative probability at x.");

    py::class_<NonCentralCumulativeChiSquareSankaranApprox>(
        m, "NonCentralCumulativeChiSquareSankaranApprox",
        "Sankaran approximation of the cumulative non-central chi-square distribution.")
        .def(py::init<Real, Real>(),
            py::arg("df"), py::arg("ncp"),
            "Constructs from the degrees of freedom and non-centrality parameter.")
        .def("__call__", &NonCentralCumulativeChiSquareSankaranApprox::operator(),
            py::arg("x"),
            "Returns the approximate cumulative probability at x.");

    py::class_<InverseNonCentralCumulativeChiSquareDistribution>(
        m, "InverseNonCentralCumulativeChiSquareDistribution",
        "Inverse cumulative non-central chi-square distribution function.")
        // The shorter overload lets QuantLib supply the solver controls.
        .def(py::init<Real, Real>(),
            py::arg("df"), py::arg("ncp"),
            "Constructs from the degrees of freedom and non-centrality parameter. "
            "The solver controls take QuantLib's own defaults.")
        .def(py::init<Real, Real, Size, Real>(),
            py::arg("df"), py::arg("ncp"),
            py::arg("maxEvaluations"), py::arg("accuracy"),
            "Constructs with explicit solver controls.")
        .def("__call__", &InverseNonCentralCumulativeChiSquareDistribution::operator(),
            py::arg("x"),
            "Returns the quantile at probability x.");
}
