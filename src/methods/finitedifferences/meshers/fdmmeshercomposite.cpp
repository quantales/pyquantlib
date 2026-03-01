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
#include <ql/methods/finitedifferences/meshers/fdmmeshercomposite.hpp>
#include <ql/methods/finitedifferences/operators/fdmlinearoplayout.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmmeshercomposite(py::module_& m) {
    py::class_<FdmMesherComposite, FdmMesher,
               ext::shared_ptr<FdmMesherComposite>>(
        m, "FdmMesherComposite",
        "Composite multi-dimensional mesher built from 1D meshers.")
        .def(py::init<const std::vector<ext::shared_ptr<Fdm1dMesher>>&>(),
            py::arg("meshers"),
            "Constructs from a vector of 1D meshers.")
        .def(py::init<const ext::shared_ptr<FdmLinearOpLayout>&,
                      const std::vector<ext::shared_ptr<Fdm1dMesher>>&>(),
            py::arg("layout"), py::arg("meshers"),
            "Constructs from a layout and vector of 1D meshers.")
        .def(py::init<const ext::shared_ptr<Fdm1dMesher>&>(),
            py::arg("mesher"),
            "Constructs a 1D composite mesher.")
        .def(py::init<const ext::shared_ptr<Fdm1dMesher>&,
                      const ext::shared_ptr<Fdm1dMesher>&>(),
            py::arg("m1"), py::arg("m2"),
            "Constructs a 2D composite mesher.")
        .def(py::init<const ext::shared_ptr<Fdm1dMesher>&,
                      const ext::shared_ptr<Fdm1dMesher>&,
                      const ext::shared_ptr<Fdm1dMesher>&>(),
            py::arg("m1"), py::arg("m2"), py::arg("m3"),
            "Constructs a 3D composite mesher.")
        .def(py::init<const ext::shared_ptr<Fdm1dMesher>&,
                      const ext::shared_ptr<Fdm1dMesher>&,
                      const ext::shared_ptr<Fdm1dMesher>&,
                      const ext::shared_ptr<Fdm1dMesher>&>(),
            py::arg("m1"), py::arg("m2"), py::arg("m3"), py::arg("m4"),
            "Constructs a 4D composite mesher.")
        .def("getFdm1dMeshers", &FdmMesherComposite::getFdm1dMeshers,
            py::return_value_policy::reference_internal,
            "Returns the underlying 1D meshers.");
}
