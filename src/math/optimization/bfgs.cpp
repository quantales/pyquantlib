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
#include <ql/math/optimization/bfgs.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::bfgs(py::module_& m) {
    py::class_<BFGS, OptimizationMethod, ext::shared_ptr<BFGS>>(
        m, "BFGS",
        "Broyden-Fletcher-Goldfarb-Shanno optimization method.")
        .def(py::init<>(),
            "Constructs with default line search.");
}
