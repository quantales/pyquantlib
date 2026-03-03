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
#include <ql/math/optimization/steepestdescent.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::steepestdescent(py::module_& m) {
    py::class_<SteepestDescent, OptimizationMethod,
               ext::shared_ptr<SteepestDescent>>(
        m, "SteepestDescent",
        "Multi-dimensional steepest descent optimization method.")
        .def(py::init<>(),
            "Constructs with default line search.");
}
