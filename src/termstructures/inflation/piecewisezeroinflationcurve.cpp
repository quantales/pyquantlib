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
#include <ql/termstructures/inflation/piecewisezeroinflationcurve.hpp>
#include <ql/termstructures/inflation/inflationhelpers.hpp>
#include <ql/termstructures/inflation/seasonality.hpp>
#include <ql/math/interpolations/linearinterpolation.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::piecewisezeroinflationcurve(py::module_& m) {
    using Curve = PiecewiseZeroInflationCurve<Linear>;
    using Helpers = std::vector<
        ext::shared_ptr<BootstrapHelper<ZeroInflationTermStructure>>>;

    py::class_<Curve, ZeroInflationTermStructure, ext::shared_ptr<Curve>>(
        m, "PiecewiseZeroInflationCurve",
        "Piecewise zero-inflation curve bootstrapped from helpers.")
        .def(py::init([](const Date& referenceDate,
                         const Date& baseDate,
                         Frequency frequency,
                         const DayCounter& dayCounter,
                         const Helpers& instruments,
                         const py::object& seasonality,
                         Real accuracy) {
            ext::shared_ptr<Seasonality> s;
            if (!seasonality.is_none())
                s = seasonality.cast<ext::shared_ptr<Seasonality>>();
            return ext::make_shared<Curve>(
                referenceDate, baseDate, frequency, dayCounter,
                instruments, s, accuracy);
        }),
            py::arg("referenceDate"),
            py::arg("baseDate"),
            py::arg("frequency"),
            py::arg("dayCounter"),
            py::arg("instruments"),
            py::arg("seasonality") = py::none(),
            py::arg("accuracy") = 1.0e-14,
            "Constructs from reference date, base date, and helpers.")
        .def("times", &Curve::times,
            py::return_value_policy::copy,
            "Returns the interpolation times.")
        .def("dates", &Curve::dates,
            py::return_value_policy::copy,
            "Returns the interpolation dates.")
        .def("data", &Curve::data,
            py::return_value_policy::copy,
            "Returns the interpolated data values.")
        .def("nodes", &Curve::nodes,
            "Returns (date, value) pairs for all nodes.");
}
