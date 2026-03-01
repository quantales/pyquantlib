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
#include <ql/methods/finitedifferences/operators/fdmlinearoplayout.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::fdmlinearoplayout(py::module_& m) {
    py::class_<FdmLinearOpLayout, ext::shared_ptr<FdmLinearOpLayout>>(
        m, "FdmLinearOpLayout",
        "Memory layout of a FDM linear operator grid.")
        .def(py::init<std::vector<Size>>(),
            py::arg("dim"),
            "Constructs from grid dimensions.")
        .def("begin", &FdmLinearOpLayout::begin,
            "Returns an iterator to the first element.")
        .def("end", &FdmLinearOpLayout::end,
            "Returns an iterator past the last element.")
        .def("dim", &FdmLinearOpLayout::dim,
            py::return_value_policy::reference_internal,
            "Returns the dimension vector.")
        .def("spacing", &FdmLinearOpLayout::spacing,
            py::return_value_policy::reference_internal,
            "Returns the spacing (stride) vector.")
        .def("size", &FdmLinearOpLayout::size,
            "Returns the total number of grid points.")
        .def("index", &FdmLinearOpLayout::index,
            py::arg("coordinates"),
            "Returns the flat index for given coordinates.")
        .def("neighbourhood",
            py::overload_cast<const FdmLinearOpIterator&, Size, Integer>(
                &FdmLinearOpLayout::neighbourhood, py::const_),
            py::arg("iterator"), py::arg("i"), py::arg("offset"),
            "Returns neighbour flat index in dimension i.")
        .def("neighbourhood",
            py::overload_cast<const FdmLinearOpIterator&,
                              Size, Integer, Size, Integer>(
                &FdmLinearOpLayout::neighbourhood, py::const_),
            py::arg("iterator"), py::arg("i1"), py::arg("offset1"),
            py::arg("i2"), py::arg("offset2"),
            "Returns neighbour flat index in dimensions i1 and i2.")
        .def("iter_neighbourhood",
            &FdmLinearOpLayout::iter_neighbourhood,
            py::arg("iterator"), py::arg("i"), py::arg("offset"),
            "Returns a neighbour iterator in dimension i.")
        .def("__len__", &FdmLinearOpLayout::size)
        // FdmLinearOpIterator lacks operator==, so py::make_iterator
        // cannot be used.  Build a list as a workaround.
        .def("__iter__", [](const FdmLinearOpLayout& layout) {
            auto it = layout.begin();
            auto end = layout.end();
            py::list result;
            while (it != end) {
                result.append(py::cast(*it));
                ++it;
            }
            return result.attr("__iter__")();
        });
}
