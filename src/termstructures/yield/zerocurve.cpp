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
#include <ql/termstructures/yield/zerocurve.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::zerocurve(py::module_& m) {
    py::class_<ZeroCurve, YieldTermStructure, ext::shared_ptr<ZeroCurve>>(
        m, "ZeroCurve",
        "Yield curve based on zero rates with linear interpolation.")
        // Constructor without calendar
        .def(py::init([](const std::vector<Date>& dates,
                         const std::vector<Rate>& yields,
                         const DayCounter& dayCounter,
                         Compounding compounding,
                         Frequency frequency) {
            return ext::make_shared<ZeroCurve>(dates, yields, dayCounter,
                                               Linear(), compounding, frequency);
        }),
            py::arg("dates"), py::arg("yields"), py::arg("dayCounter"),
            py::arg("compounding") = Continuous,
            py::arg("frequency") = Annual,
            "Constructs from dates, yields, and day counter.")
        // Constructor with calendar
        .def(py::init([](const std::vector<Date>& dates,
                         const std::vector<Rate>& yields,
                         const DayCounter& dayCounter,
                         const Calendar& calendar,
                         Compounding compounding,
                         Frequency frequency) {
            return ext::make_shared<ZeroCurve>(dates, yields, dayCounter,
                                               calendar, Linear(),
                                               compounding, frequency);
        }),
            py::arg("dates"), py::arg("yields"), py::arg("dayCounter"),
            py::arg("calendar"),
            py::arg("compounding") = Continuous,
            py::arg("frequency") = Annual,
            "Constructs from dates, yields, day counter, and calendar.")
        .def("dates", &ZeroCurve::dates,
             py::return_value_policy::reference_internal,
             "Returns the curve dates.")
        .def("data", &ZeroCurve::data,
             py::return_value_policy::reference_internal,
             "Returns the zero rates.")
        .def("zeroRates", &ZeroCurve::zeroRates,
             py::return_value_policy::reference_internal,
             "Returns the zero rates.")
        .def("times", &ZeroCurve::times,
             py::return_value_policy::reference_internal,
             "Returns the curve times.")
        .def("nodes", &ZeroCurve::nodes,
             "Returns the (date, rate) pairs.");
}
