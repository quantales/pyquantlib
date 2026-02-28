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
#include <ql/math/randomnumbers/haltonrsg.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_math::haltonrsg(py::module_& m) {
    py::class_<HaltonRsg>(m, "HaltonRsg",
        "Halton low-discrepancy sequence generator.")
        .def(py::init<Size, unsigned long, bool, bool>(),
            py::arg("dimensionality"),
            py::arg("seed") = 0,
            py::arg("randomStart") = true,
            py::arg("randomShift") = false,
            "Constructs Halton sequence generator.")
        .def("nextSequence", &HaltonRsg::nextSequence,
            py::return_value_policy::copy,
            "Returns next sample sequence.")
        .def("lastSequence", &HaltonRsg::lastSequence,
            py::return_value_policy::copy,
            "Returns the last generated sequence.")
        .def("dimension", &HaltonRsg::dimension,
            "Returns the dimensionality.");
}
