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
#include <ql/methods/finitedifferences/utilities/squarerootprocessrndcalculator.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::squarerootprocessrndcalculator(py::module_& m) {
    py::class_<SquareRootProcessRNDCalculator,
               ext::shared_ptr<SquareRootProcessRNDCalculator>,
               RiskNeutralDensityCalculator>(
        m, "SquareRootProcessRNDCalculator",
        "Square-root process risk-neutral density calculator.")
        .def(py::init<Real, Real, Real, Real>(),
            py::arg("v0"), py::arg("kappa"),
            py::arg("theta"), py::arg("sigma"),
            "Constructs with initial value, mean reversion, long-run mean, and volatility.")
        .def("stationary_pdf", &SquareRootProcessRNDCalculator::stationary_pdf,
            py::arg("v"),
            "Returns stationary probability density at v.")
        .def("stationary_cdf", &SquareRootProcessRNDCalculator::stationary_cdf,
            py::arg("v"),
            "Returns stationary cumulative distribution at v.")
        .def("stationary_invcdf", &SquareRootProcessRNDCalculator::stationary_invcdf,
            py::arg("q"),
            "Returns stationary inverse CDF at quantile q.");
}
