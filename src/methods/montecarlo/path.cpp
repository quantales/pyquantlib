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
#include <ql/methods/montecarlo/path.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::path(py::module_& m) {
    py::class_<Path>(m, "Path",
        "Single-factor random walk.")
        .def(py::init<const TimeGrid&, Array>(),
            py::arg("timeGrid"), py::arg("values") = Array(),
            "Constructs a path on the given time grid.")
        .def("empty", &Path::empty, "True if path is empty.")
        .def("length", &Path::length, "Number of points in the path.")
        .def("__len__", &Path::length)
        .def("__getitem__", [](const Path& p, int i) {
            if (i < 0) i += static_cast<int>(p.length());
            if (i < 0 || static_cast<Size>(i) >= p.length())
                throw py::index_error("Path index out of range");
            return p[i];
        }, py::arg("i"), "Returns value at index i.")
        .def("value", [](const Path& p, Size i) { return p.value(i); },
            py::arg("i"), "Returns value at index i.")
        .def("time", &Path::time, py::arg("i"),
            "Returns time at index i.")
        .def("front", [](const Path& p) { return p.front(); },
            "Returns first value.")
        .def("back", [](const Path& p) { return p.back(); },
            "Returns last value.")
        .def("timeGrid", &Path::timeGrid,
            py::return_value_policy::reference_internal,
            "Returns the underlying time grid.")
        .def("__repr__", [](const Path& p) {
            return "Path(length=" + std::to_string(p.length()) + ")";
        });
}
