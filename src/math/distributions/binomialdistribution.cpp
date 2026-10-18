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
#include <ql/math/distributions/binomialdistribution.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::binomialdistribution(py::module_& m) {
    py::class_<BinomialDistribution>(
        m, "BinomialDistribution",
        "Binomial probability mass function.")
        .def(py::init<Real, BigNatural>(),
            py::arg("p"), py::arg("n"),
            "Constructs from the success probability and number of trials.")
        .def("__call__", &BinomialDistribution::operator(),
            py::arg("k"),
            "Returns the probability of k successes.");

    py::class_<CumulativeBinomialDistribution>(
        m, "CumulativeBinomialDistribution",
        "Cumulative binomial distribution function.")
        .def(py::init<Real, BigNatural>(),
            py::arg("p"), py::arg("n"),
            "Constructs from the success probability and number of trials.")
        .def("__call__", &CumulativeBinomialDistribution::operator(),
            py::arg("k"),
            "Returns the probability of at most k successes.");

    m.def("binomialCoefficient", &binomialCoefficient,
        py::arg("n"), py::arg("k"),
        "Returns the binomial coefficient n choose k.");
    m.def("binomialCoefficientLn", &binomialCoefficientLn,
        py::arg("n"), py::arg("k"),
        "Returns the logarithm of the binomial coefficient n choose k.");
    m.def("PeizerPrattMethod2Inversion", &PeizerPrattMethod2Inversion,
        py::arg("z"), py::arg("n"),
        "Returns the Peizer-Pratt method 2 inversion of the binomial distribution.");
}
