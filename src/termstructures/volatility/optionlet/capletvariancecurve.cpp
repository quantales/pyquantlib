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
#include <ql/termstructures/volatility/optionlet/capletvariancecurve.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::capletvariancecurve(py::module_& m) {
    py::class_<CapletVarianceCurve, OptionletVolatilityStructure,
               ext::shared_ptr<CapletVarianceCurve>>(
        m, "CapletVarianceCurve",
        "Caplet volatility curve modelled as a variance curve, no strike dependence.")
        .def(py::init<const Date&, const std::vector<Date>&,
                      const std::vector<Volatility>&, const DayCounter&,
                      VolatilityType, Real>(),
            py::arg("referenceDate"), py::arg("dates"),
            py::arg("capletVolCurve"), py::arg("dayCounter"),
            py::arg("type") = ShiftedLognormal, py::arg("displacement") = 0.0,
            "Constructs from reference date, dates, and caplet volatilities.")
        .def("dayCounter", &CapletVarianceCurve::dayCounter,
            "Returns the day counter.")
        .def("maxDate", &CapletVarianceCurve::maxDate,
            "Returns the maximum date.")
        .def("minStrike", &CapletVarianceCurve::minStrike,
            "Returns the minimum strike.")
        .def("maxStrike", &CapletVarianceCurve::maxStrike,
            "Returns the maximum strike.");
}
