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
#include <ql/methods/finitedifferences/meshers/fdmmesher.hpp>
#include <ql/methods/finitedifferences/operators/fdmlinearoplayout.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmmesher(py::module_& m) {
    py::class_<FdmMesher, ext::shared_ptr<FdmMesher>>(
        m, "FdmMesher",
        "Abstract base class for multi-dimensional FDM meshers.")
        .def("layout", &FdmMesher::layout,
            py::return_value_policy::reference_internal,
            "Returns the grid layout.")
        .def("dplus", &FdmMesher::dplus,
            py::arg("iter"), py::arg("direction"),
            "Returns the forward difference at iterator position.")
        .def("dminus", &FdmMesher::dminus,
            py::arg("iter"), py::arg("direction"),
            "Returns the backward difference at iterator position.")
        .def("location", &FdmMesher::location,
            py::arg("iter"), py::arg("direction"),
            "Returns the location at iterator position.")
        .def("locations", &FdmMesher::locations,
            py::arg("direction"),
            "Returns all locations along a direction.");
}
