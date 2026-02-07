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
#include <ql/math/distributions/bivariatenormaldistribution.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::bivariatenormaldistribution(py::module_& m) {
    py::class_<BivariateCumulativeNormalDistributionWe04DP>(
        m, "BivariateCumulativeNormalDistribution",
        "Cumulative bivariate normal distribution (West 2004).")
        .def(py::init<Real>(),
            py::arg("rho"),
            "Constructs BivariateCumulativeNormalDistribution with correlation rho.")
        .def("__call__", &BivariateCumulativeNormalDistributionWe04DP::operator(),
            py::arg("x"), py::arg("y"),
            "Returns the cumulative bivariate normal probability.");
}
