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
#include "pyquantlib/trampolines.h"
#include <ql/math/optimization/method.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::optimizationmethod(py::module_& m) {
    py::class_<OptimizationMethod, PyOptimizationMethod, ext::shared_ptr<OptimizationMethod>>(
        m, "OptimizationMethod",
        "Abstract base class for optimization methods.")
        .def(py::init_alias<>())
        .def("minimize", &OptimizationMethod::minimize,
            py::arg("problem"), py::arg("endCriteria"),
            "Minimizes the problem using the given end criteria.");
}
