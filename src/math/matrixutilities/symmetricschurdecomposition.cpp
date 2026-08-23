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
#include <ql/math/matrixutilities/symmetricschurdecomposition.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::symmetricschurdecomposition(py::module_& m) {
    py::class_<SymmetricSchurDecomposition>(
        m, "SymmetricSchurDecomposition",
        "Symmetric Schur decomposition (eigenvalue decomposition).")
        .def(py::init<const Matrix&>(),
            py::arg("matrix"),
            "Constructs decomposition from a symmetric matrix.")
        .def("eigenvalues", &SymmetricSchurDecomposition::eigenvalues,
            py::return_value_policy::reference_internal,
            "Returns the eigenvalues in decreasing order.")
        .def("eigenvectors", &SymmetricSchurDecomposition::eigenvectors,
            py::return_value_policy::reference_internal,
            "Returns the eigenvector matrix.");
}
