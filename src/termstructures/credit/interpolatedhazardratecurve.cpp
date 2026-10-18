/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/termstructures/credit/interpolatedhazardratecurve.hpp>
#include <ql/math/interpolations/backwardflatinterpolation.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::interpolatedhazardratecurve(py::module_& m) {
    using Curve = InterpolatedHazardRateCurve<BackwardFlat>;

    py::class_<Curve, DefaultProbabilityTermStructure, ext::shared_ptr<Curve>>(
        m, "HazardRateCurve",
        "Hazard rate curve with backward-flat (piecewise constant) interpolation of the hazard rates.")
        .def(py::init([](const std::vector<Date>& dates,
                         const std::vector<Real>& hazardRates,
                         const DayCounter& dayCounter) {
            return ext::make_shared<Curve>(dates, hazardRates, dayCounter);
        }),
            py::arg("dates"), py::arg("hazardRates"), py::arg("dayCounter"),
            "Constructs from dates, hazard rates, and day counter.")
        .def(py::init([](const std::vector<Date>& dates,
                         const std::vector<Real>& hazardRates,
                         const DayCounter& dayCounter,
                         const Calendar& calendar,
                         const std::vector<Handle<Quote>>& jumps,
                         const std::vector<Date>& jumpDates) {
            return ext::make_shared<Curve>(dates, hazardRates, dayCounter,
                                           calendar, jumps, jumpDates);
        }),
            py::arg("dates"), py::arg("hazardRates"), py::arg("dayCounter"),
            py::arg("calendar"),
            py::arg("jumps") = std::vector<Handle<Quote>>(),
            py::arg("jumpDates") = std::vector<Date>(),
            "Constructs from dates, hazard rates, day counter, calendar, and optional jumps.")
        .def("dates", &Curve::dates,
            py::return_value_policy::reference_internal,
            "Returns the curve dates.")
        .def("times", &Curve::times,
            py::return_value_policy::reference_internal,
            "Returns the curve times.")
        .def("data", &Curve::data,
            py::return_value_policy::reference_internal,
            "Returns the curve values.")
        .def("hazardRates", &Curve::hazardRates,
            py::return_value_policy::reference_internal,
            "Returns the hazard rates.")
        .def("nodes", &Curve::nodes,
            "Returns the (date, value) pairs.");
}
