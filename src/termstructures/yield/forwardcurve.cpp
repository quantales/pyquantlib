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
#include <ql/termstructures/yield/forwardcurve.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::forwardcurve(py::module_& m) {
    py::class_<ForwardCurve, YieldTermStructure, ext::shared_ptr<ForwardCurve>>(
        m, "ForwardCurve",
        "Yield curve based on forward rates with backward-flat interpolation.")
        // Constructor without calendar
        .def(py::init([](const std::vector<Date>& dates,
                         const std::vector<Rate>& forwards,
                         const DayCounter& dayCounter) {
            return ext::make_shared<ForwardCurve>(dates, forwards, dayCounter,
                                                   BackwardFlat());
        }),
            py::arg("dates"), py::arg("forwards"), py::arg("dayCounter"),
            "Constructs from dates, forward rates, and day counter.")
        // Constructor with calendar
        .def(py::init([](const std::vector<Date>& dates,
                         const std::vector<Rate>& forwards,
                         const DayCounter& dayCounter,
                         const Calendar& calendar) {
            return ext::make_shared<ForwardCurve>(dates, forwards, dayCounter,
                                                   calendar, BackwardFlat());
        }),
            py::arg("dates"), py::arg("forwards"), py::arg("dayCounter"),
            py::arg("calendar"),
            "Constructs from dates, forward rates, day counter, and calendar.")
        .def("dates", &ForwardCurve::dates,
             py::return_value_policy::reference_internal,
             "Returns the curve dates.")
        .def("data", &ForwardCurve::data,
             py::return_value_policy::reference_internal,
             "Returns the forward rates.")
        .def("forwards", &ForwardCurve::forwards,
             py::return_value_policy::reference_internal,
             "Returns the forward rates.")
        .def("times", &ForwardCurve::times,
             py::return_value_policy::reference_internal,
             "Returns the curve times.")
        .def("nodes", &ForwardCurve::nodes,
             "Returns the (date, forward rate) pairs.");
}
