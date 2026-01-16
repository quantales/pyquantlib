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
#include <ql/math/optimization/levenbergmarquardt.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::levenbergmarquardt(py::module_& m) {
    py::class_<LevenbergMarquardt, OptimizationMethod, ext::shared_ptr<LevenbergMarquardt>>(
        m, "LevenbergMarquardt",
        "Levenberg-Marquardt optimization method.")
        .def(py::init<Real, Real, Real>(),
            py::arg("epsfcn") = 1.0e-8,
            py::arg("xtol") = 1.0e-8,
            py::arg("gtol") = 1.0e-8,
            "Creates a Levenberg-Marquardt optimizer.");
}
