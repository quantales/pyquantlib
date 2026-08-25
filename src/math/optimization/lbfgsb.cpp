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
#include <ql/math/optimization/lbfgsb.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::lbfgsb(py::module_& m) {
    py::class_<LBFGSB, OptimizationMethod, ext::shared_ptr<LBFGSB>>(
        m, "LBFGSB",
        "Limited-memory BFGS for bound-constrained optimization.")
        .def(py::init<Size, Real, Real>(),
            py::arg("memory") = 10,
            py::arg("pgTol") = 1.0e-8,
            py::arg("fTol") = 1.0e7 * QL_EPSILON,
            "Creates an L-BFGS-B optimizer using the problem's constraint bounds.")
        .def(py::init<Array, Array, Size, Real, Real>(),
            py::arg("lowerBound"),
            py::arg("upperBound"),
            py::arg("memory") = 10,
            py::arg("pgTol") = 1.0e-8,
            py::arg("fTol") = 1.0e7 * QL_EPSILON,
            "Creates an L-BFGS-B optimizer with explicit box bounds, which "
            "override the problem's constraint. Use +/- DBL_MAX for unbounded "
            "coordinates.");
}
