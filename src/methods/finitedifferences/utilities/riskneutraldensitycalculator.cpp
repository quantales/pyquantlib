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
#include <ql/methods/finitedifferences/utilities/riskneutraldensitycalculator.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::riskneutraldensitycalculator(py::module_& m) {
    py::class_<RiskNeutralDensityCalculator,
               ext::shared_ptr<RiskNeutralDensityCalculator>>(
        m, "RiskNeutralDensityCalculator",
        "Abstract base for risk-neutral density calculations.")
        .def("pdf", &RiskNeutralDensityCalculator::pdf,
            py::arg("x"), py::arg("t"),
            "Returns probability density function at x and time t.")
        .def("cdf", &RiskNeutralDensityCalculator::cdf,
            py::arg("x"), py::arg("t"),
            "Returns cumulative distribution function at x and time t.")
        .def("invcdf", &RiskNeutralDensityCalculator::invcdf,
            py::arg("p"), py::arg("t"),
            "Returns inverse CDF at probability p and time t.");
}
