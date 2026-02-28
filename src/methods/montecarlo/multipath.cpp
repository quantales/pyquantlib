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
#include <ql/methods/montecarlo/multipath.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::multipath(py::module_& m) {
    py::class_<MultiPath>(m, "MultiPath",
        "Correlated multiple asset paths.")
        .def(py::init<Size, const TimeGrid&>(),
            py::arg("nAsset"), py::arg("timeGrid"),
            "Constructs paths for nAsset assets on the given time grid.")
        .def(py::init<std::vector<Path>>(),
            py::arg("paths"),
            "Constructs from a vector of single-asset paths.")
        .def("assetNumber", &MultiPath::assetNumber,
            "Number of assets.")
        .def("pathSize", &MultiPath::pathSize,
            "Number of points in each path.")
        .def("__len__", &MultiPath::assetNumber)
        .def("__getitem__", [](const MultiPath& mp, int j) -> const Path& {
            if (j < 0) j += static_cast<int>(mp.assetNumber());
            if (j < 0 || static_cast<Size>(j) >= mp.assetNumber())
                throw py::index_error("MultiPath index out of range");
            return mp[j];
        }, py::arg("j"), py::return_value_policy::reference_internal,
            "Returns the path for asset j.")
        .def("__repr__", [](const MultiPath& mp) {
            return "MultiPath(assets=" + std::to_string(mp.assetNumber()) +
                   ", pathSize=" + std::to_string(mp.pathSize()) + ")";
        });
}
