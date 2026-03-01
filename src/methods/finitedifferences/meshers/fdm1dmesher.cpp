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
#include <ql/methods/finitedifferences/meshers/fdm1dmesher.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdm1dmesher(py::module_& m) {
    py::class_<Fdm1dMesher, ext::shared_ptr<Fdm1dMesher>>(
        m, "Fdm1dMesher",
        "Base class for one-dimensional FDM meshers.")
        .def(py::init<Size>(),
            py::arg("size"),
            "Constructs a 1D mesher of the given size.")
        .def("size", &Fdm1dMesher::size,
            "Returns the number of grid points.")
        .def("dplus", &Fdm1dMesher::dplus,
            py::arg("index"),
            "Returns the forward difference at index.")
        .def("dminus", &Fdm1dMesher::dminus,
            py::arg("index"),
            "Returns the backward difference at index.")
        .def("location", &Fdm1dMesher::location,
            py::arg("index"),
            "Returns the location at index.")
        .def("locations", &Fdm1dMesher::locations,
            py::return_value_policy::reference_internal,
            "Returns all grid locations.")
        .def("__len__", &Fdm1dMesher::size);
}
