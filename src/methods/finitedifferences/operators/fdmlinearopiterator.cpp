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
#include <ql/methods/finitedifferences/operators/fdmlinearopiterator.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmlinearopiterator(py::module_& m) {
    py::class_<FdmLinearOpIterator>(m, "FdmLinearOpIterator",
        "Iterator for a FDM linear operator layout.")
        .def(py::init<Size>(),
            py::arg("index") = 0,
            "Constructs with a flat index.")
        .def(py::init<std::vector<Size>>(),
            py::arg("dim"),
            "Constructs from grid dimensions.")
        .def(py::init<std::vector<Size>, std::vector<Size>, Size>(),
            py::arg("dim"), py::arg("coordinates"), py::arg("index"),
            "Constructs from dimensions, coordinates, and flat index.")
        .def("index", &FdmLinearOpIterator::index,
            "Returns the flat index.")
        .def("coordinates", &FdmLinearOpIterator::coordinates,
            py::return_value_policy::reference_internal,
            "Returns the coordinate vector.")
        .def("increment", [](FdmLinearOpIterator& self) { ++self; },
            "Advances the iterator by one position.")
        .def("notEqual", [](const FdmLinearOpIterator& self,
                            const FdmLinearOpIterator& other) {
            return self != other;
        }, py::arg("other"),
            "Returns true if iterators differ.");
}
