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
#include <ql/methods/finitedifferences/meshers/uniform1dmesher.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::uniform1dmesher(py::module_& m) {
    py::class_<Uniform1dMesher, Fdm1dMesher,
               ext::shared_ptr<Uniform1dMesher>>(
        m, "Uniform1dMesher",
        "One-dimensional uniform grid mesher.")
        .def(py::init<Real, Real, Size>(),
            py::arg("start"), py::arg("end"), py::arg("size"),
            "Constructs a uniform grid from start to end.");
}
