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
#include <ql/math/matrixutilities/svd.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::svd(py::module_& m) {
    py::class_<SVD>(m, "SVD",
        "Singular value decomposition of a matrix.")
        .def(py::init<const Matrix&>(),
            py::arg("matrix"),
            "Constructs SVD from a matrix.")
        .def("U", &SVD::U,
            py::return_value_policy::reference_internal,
            "Returns the U matrix.")
        .def("V", &SVD::V,
            py::return_value_policy::reference_internal,
            "Returns the V matrix.")
        .def("singularValues", &SVD::singularValues,
            py::return_value_policy::reference_internal,
            "Returns the singular values.")
        .def("S", &SVD::S,
            "Returns the diagonal matrix of singular values.")
        .def("norm2", &SVD::norm2,
            "Returns the 2-norm (largest singular value).")
        .def("cond", &SVD::cond,
            "Returns the condition number.")
        .def("rank", &SVD::rank,
            "Returns the numerical rank.")
        .def("solveFor", &SVD::solveFor,
            py::arg("b"),
            "Solves Ax = b using the SVD.");
}
