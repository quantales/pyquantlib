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
#include <ql/math/copulas/claytoncopula.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::claytoncopula(py::module_& m) {
    py::class_<ClaytonCopula>(
        m, "ClaytonCopula",
        "Clayton copula.")
        .def(py::init<Real>(),
            py::arg("theta"),
            "Constructs from the copula parameter.")
        .def("__call__", &ClaytonCopula::operator(),
            py::arg("x"), py::arg("y"),
            "Returns the copula value C(x, y).");
}
