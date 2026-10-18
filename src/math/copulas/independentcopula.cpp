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
#include <ql/math/copulas/independentcopula.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::independentcopula(py::module_& m) {
    py::class_<IndependentCopula>(
        m, "IndependentCopula",
        "Independent copula.")
        .def(py::init<>())
        .def("__call__", &IndependentCopula::operator(),
            py::arg("x"), py::arg("y"),
            "Returns the copula value C(x, y).");
}
