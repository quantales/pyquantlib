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
#include <ql/methods/finitedifferences/utilities/cevrndcalculator.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::cevrndcalculator(py::module_& m) {
    py::class_<CEVRNDCalculator,
               ext::shared_ptr<CEVRNDCalculator>,
               RiskNeutralDensityCalculator>(
        m, "CEVRNDCalculator",
        "Constant Elasticity of Variance risk-neutral density calculator.")
        .def(py::init<Real, Real, Real>(),
            py::arg("f0"), py::arg("alpha"), py::arg("beta"),
            "Constructs with forward price, alpha, and beta.")
        .def("massAtZero", &CEVRNDCalculator::massAtZero,
            py::arg("t"),
            "Returns probability mass at zero for time t.");
}
