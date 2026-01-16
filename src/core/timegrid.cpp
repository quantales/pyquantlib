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
#include <ql/timegrid.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::timegrid(py::module_& m) {
    py::class_<TimeGrid>(m, "TimeGrid", "Time grid for discretized models.")
        .def(py::init<>(),
            "Default constructor.")
        .def(py::init<Time, Size>(),
            py::arg("end"), py::arg("steps"),
            "Constructs a regularly spaced time grid.")
        .def(py::init([](const std::vector<Time>& times) {
                return std::make_unique<TimeGrid>(times.begin(), times.end());
            }),
            py::arg("times"),
            "Constructs from mandatory time points.")
        .def(py::init([](const std::vector<Time>& times, Size steps) {
                return std::make_unique<TimeGrid>(times.begin(), times.end(), steps);
            }),
            py::arg("times"), py::arg("steps"),
            "Constructs from mandatory time points with minimum steps.")
        .def("index", &TimeGrid::index,
            py::arg("t"),
            "Returns the index i such that grid[i] = t.")
        .def("closestIndex", &TimeGrid::closestIndex,
            py::arg("t"),
            "Returns the index of the time closest to t.")
        .def("closestTime", &TimeGrid::closestTime,
            py::arg("t"),
            "Returns the time on the grid closest to t.")
        .def("mandatoryTimes", &TimeGrid::mandatoryTimes,
            py::return_value_policy::copy,
            "Returns the mandatory time points.")
        .def("dt", &TimeGrid::dt,
            py::arg("i"),
            "Returns the time step dt(i) = t(i+1) - t(i).")
        .def("size", &TimeGrid::size,
            "Returns the number of time points.")
        .def("empty", &TimeGrid::empty,
            "Returns true if the grid is empty.")
        .def("at", &TimeGrid::at,
            py::arg("i"),
            "Returns the time at index i with bounds checking.")
        .def("front", &TimeGrid::front,
            "Returns the first time (t=0).")
        .def("back", &TimeGrid::back,
            "Returns the last time.")
        .def("__len__", &TimeGrid::size)
        .def("__getitem__",
            py::overload_cast<Size>(&TimeGrid::operator[], py::const_),
            py::arg("i"))
        .def("__iter__", [](const TimeGrid& tg) {
                return py::make_iterator(tg.begin(), tg.end());
            }, py::keep_alive<0, 1>());
}
