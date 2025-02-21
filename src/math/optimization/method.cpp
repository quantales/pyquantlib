/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 * 
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 * 
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
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
