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
#include <ql/methods/finitedifferences/meshers/predefined1dmesher.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::predefined1dmesher(py::module_& m) {
    py::class_<Predefined1dMesher, Fdm1dMesher,
               ext::shared_ptr<Predefined1dMesher>>(
        m, "Predefined1dMesher",
        "One-dimensional mesher from predefined grid points.")
        .def(py::init<const std::vector<Real>&>(),
            py::arg("x"),
            "Constructs from explicit grid locations.");
}
