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
#include <ql/termstructures/inflation/interpolatedyoyinflationcurve.hpp>
#include <ql/termstructures/inflation/seasonality.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::interpolatedyoyinflationcurve(py::module_& m) {
    using Curve = YoYInflationCurve;  // InterpolatedYoYInflationCurve<Linear>

    py::class_<Curve, YoYInflationTermStructure, ext::shared_ptr<Curve>>(
        m, "YoYInflationCurve",
        "Year-on-year inflation curve with linear interpolation.")
        .def(py::init([](const Date& referenceDate,
                         const std::vector<Date>& dates,
                         const std::vector<Rate>& rates,
                         Frequency frequency,
                         const DayCounter& dayCounter,
                         const py::object& seasonality) {
            ext::shared_ptr<Seasonality> s;
            if (!seasonality.is_none())
                s = seasonality.cast<ext::shared_ptr<Seasonality>>();
            return ext::make_shared<Curve>(
                referenceDate, dates, rates, frequency, dayCounter, s);
        }),
            py::arg("referenceDate"),
            py::arg("dates"),
            py::arg("rates"),
            py::arg("frequency"),
            py::arg("dayCounter"),
            py::arg("seasonality") = py::none(),
            "Constructs from dates and year-on-year rates.")
        .def("dates", &Curve::dates,
            py::return_value_policy::copy,
            "Returns the interpolation dates.")
        .def("times", &Curve::times,
            py::return_value_policy::copy,
            "Returns the interpolation times.")
        .def("data", &Curve::data,
            py::return_value_policy::copy,
            "Returns the interpolated data values.")
        .def("rates", &Curve::rates,
            py::return_value_policy::copy,
            "Returns the year-on-year rates.")
        .def("nodes", &Curve::nodes,
            "Returns (date, rate) pairs for all nodes.");
}
