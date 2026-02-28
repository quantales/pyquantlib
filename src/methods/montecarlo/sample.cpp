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
#include <ql/methods/montecarlo/sample.hpp>
#include <ql/methods/montecarlo/path.hpp>
#include <ql/methods/montecarlo/multipath.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::sample(py::module_& m) {
    py::class_<Sample<Real>>(m, "SampleNumber",
        "Weighted scalar sample (value + weight).")
        .def(py::init<Real, Real>(),
            py::arg("value"), py::arg("weight"),
            "Constructs a weighted scalar sample.")
        .def_readwrite("value", &Sample<Real>::value, "Sample value.")
        .def_readwrite("weight", &Sample<Real>::weight, "Sample weight.")
        .def("__repr__", [](const Sample<Real>& s) {
            return "SampleNumber(value=" + std::to_string(s.value) +
                   ", weight=" + std::to_string(s.weight) + ")";
        });

    py::class_<Sample<std::vector<Real>>>(m, "SampleRealVector",
        "Weighted vector sample (value + weight).")
        .def(py::init<std::vector<Real>, Real>(),
            py::arg("value"), py::arg("weight"),
            "Constructs a weighted vector sample.")
        .def_readwrite("value", &Sample<std::vector<Real>>::value,
            "Sample values.")
        .def_readwrite("weight", &Sample<std::vector<Real>>::weight,
            "Sample weight.")
        .def("__repr__", [](const Sample<std::vector<Real>>& s) {
            return "SampleRealVector(dim=" + std::to_string(s.value.size()) +
                   ", weight=" + std::to_string(s.weight) + ")";
        });

    py::class_<Sample<Path>>(m, "SamplePath",
        "Weighted path sample (value + weight).")
        .def_readwrite("value", &Sample<Path>::value, "Sample path.")
        .def_readwrite("weight", &Sample<Path>::weight, "Sample weight.")
        .def("__repr__", [](const Sample<Path>& s) {
            return "SamplePath(length=" +
                   std::to_string(s.value.length()) +
                   ", weight=" + std::to_string(s.weight) + ")";
        });

    py::class_<Sample<MultiPath>>(m, "SampleMultiPath",
        "Weighted multi-path sample (value + weight).")
        .def_readwrite("value", &Sample<MultiPath>::value,
            "Sample multi-path.")
        .def_readwrite("weight", &Sample<MultiPath>::weight,
            "Sample weight.")
        .def("__repr__", [](const Sample<MultiPath>& s) {
            return "SampleMultiPath(assets=" +
                   std::to_string(s.value.assetNumber()) +
                   ", weight=" + std::to_string(s.weight) + ")";
        });
}
