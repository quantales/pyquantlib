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
#include <ql/math/optimization/simplex.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::simplex(py::module_& m) {
    py::class_<Simplex, OptimizationMethod, ext::shared_ptr<Simplex>>(
        m, "Simplex",
        "Multi-dimensional simplex optimization method.")
        .def(py::init<Real>(),
            py::arg("lambda_"),
            "Constructs with the characteristic length scale lambda.")
        .def("lambda_", &Simplex::lambda,
            "Returns the characteristic length scale.");
}
