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
#include <ql/methods/montecarlo/brownianbridge.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_methods::brownianbridge(py::module_& m) {
    py::class_<BrownianBridge>(m, "BrownianBridge",
        "Builds Wiener process paths using Gaussian variates.")
        .def(py::init<Size>(),
            py::arg("steps"),
            "Constructs a bridge with the given number of unit-time steps.")
        .def(py::init<const TimeGrid&>(),
            py::arg("timeGrid"),
            "Constructs a bridge from a time grid.")
        .def(py::init<const std::vector<Time>&>(),
            py::arg("times"),
            "Constructs a bridge from step times.")
        .def("size", &BrownianBridge::size, "Number of steps.")
        .def("times", &BrownianBridge::times,
            py::return_value_policy::reference_internal,
            "Step times.")
        .def("bridgeIndex", &BrownianBridge::bridgeIndex,
            py::return_value_policy::reference_internal,
            "Bridge construction indices.")
        .def("leftIndex", &BrownianBridge::leftIndex,
            py::return_value_policy::reference_internal,
            "Left interpolation indices.")
        .def("rightIndex", &BrownianBridge::rightIndex,
            py::return_value_policy::reference_internal,
            "Right interpolation indices.")
        .def("leftWeight", &BrownianBridge::leftWeight,
            py::return_value_policy::reference_internal,
            "Left interpolation weights.")
        .def("rightWeight", &BrownianBridge::rightWeight,
            py::return_value_policy::reference_internal,
            "Right interpolation weights.")
        .def("stdDeviation", &BrownianBridge::stdDeviation,
            py::return_value_policy::reference_internal,
            "Standard deviations.")
        .def("transform", [](const BrownianBridge& bb,
                             const std::vector<Real>& input) {
            std::vector<Real> output(bb.size());
            bb.transform(input.begin(), input.end(), output.begin());
            return output;
        }, py::arg("input"),
            "Transforms random variates into Brownian bridge path variations.")
        .def("__repr__", [](const BrownianBridge& bb) {
            return "BrownianBridge(size=" + std::to_string(bb.size()) + ")";
        });
}
