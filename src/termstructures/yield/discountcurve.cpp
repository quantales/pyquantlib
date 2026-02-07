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
#include <ql/termstructures/yield/discountcurve.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::discountcurve(py::module_& m) {
    py::class_<DiscountCurve, YieldTermStructure, ext::shared_ptr<DiscountCurve>>(
        m, "DiscountCurve",
        "Yield curve based on discount factors with log-linear interpolation.")
        // Constructor without calendar
        .def(py::init([](const std::vector<Date>& dates,
                         const std::vector<DiscountFactor>& dfs,
                         const DayCounter& dayCounter) {
            return ext::make_shared<DiscountCurve>(dates, dfs, dayCounter,
                                                    LogLinear());
        }),
            py::arg("dates"), py::arg("discounts"), py::arg("dayCounter"),
            "Constructs from dates, discount factors, and day counter.")
        // Constructor with calendar
        .def(py::init([](const std::vector<Date>& dates,
                         const std::vector<DiscountFactor>& dfs,
                         const DayCounter& dayCounter,
                         const Calendar& calendar) {
            return ext::make_shared<DiscountCurve>(dates, dfs, dayCounter,
                                                    calendar, LogLinear());
        }),
            py::arg("dates"), py::arg("discounts"), py::arg("dayCounter"),
            py::arg("calendar"),
            "Constructs from dates, discount factors, day counter, and calendar.")
        .def("dates", &DiscountCurve::dates,
             py::return_value_policy::reference_internal,
             "Returns the curve dates.")
        .def("data", &DiscountCurve::data,
             py::return_value_policy::reference_internal,
             "Returns the discount factors.")
        .def("discounts", &DiscountCurve::discounts,
             py::return_value_policy::reference_internal,
             "Returns the discount factors.")
        .def("times", &DiscountCurve::times,
             py::return_value_policy::reference_internal,
             "Returns the curve times.")
        .def("nodes", &DiscountCurve::nodes,
             "Returns the (date, discount factor) pairs.");
}
