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
#include <ql/termstructures/volatility/equityfx/blackvariancecurve.hpp>
#include <ql/math/interpolations/linearinterpolation.hpp>
#include <ql/math/interpolations/cubicinterpolation.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <algorithm>
#include <cctype>

namespace py = pybind11;
using namespace QuantLib;

namespace {
    std::string toLower(std::string s) {
        std::transform(s.begin(), s.end(), s.begin(),
                       [](unsigned char c) { return std::tolower(c); });
        return s;
    }
}

void ql_termstructures::blackvariancecurve(py::module_& m) {
    py::class_<BlackVarianceCurve, BlackVarianceTermStructure,
               ext::shared_ptr<BlackVarianceCurve>>(
        m, "BlackVarianceCurve",
        "Black volatility curve modelled as a variance curve (ATM volatilities by date).")
        .def(py::init<const Date&, const std::vector<Date>&,
                      const std::vector<Volatility>&, DayCounter, bool,
                      BlackVolTimeExtrapolation::Type>(),
            py::arg("referenceDate"),
            py::arg("dates"),
            py::arg("blackVolCurve"),
            py::arg("dayCounter"),
            py::arg("forceMonotoneVariance") = true,
            py::arg("timeExtrapolationType") = BlackVolTimeExtrapolation::FlatVolatility,
            "Constructs from reference date, dates, and ATM Black volatilities.")
        .def("dayCounter", &BlackVarianceCurve::dayCounter,
            "Returns the day counter.")
        .def("maxDate", &BlackVarianceCurve::maxDate,
            "Returns the maximum date.")
        .def("minStrike", &BlackVarianceCurve::minStrike,
            "Returns the minimum strike.")
        .def("maxStrike", &BlackVarianceCurve::maxStrike,
            "Returns the maximum strike.")
        .def("setInterpolation",
            [](BlackVarianceCurve& self, const std::string& interpolator) {
                std::string s = toLower(interpolator);
                if (s == "linear") {
                    self.setInterpolation<Linear>();
                } else if (s == "cubic") {
                    self.setInterpolation<Cubic>();
                } else {
                    throw std::invalid_argument(
                        "Unknown interpolator: " + interpolator +
                        ". Supported: 'linear', 'cubic'");
                }
            },
            py::arg("interpolator"),
            "Sets the variance interpolation. Supported: 'linear', 'cubic'.");
}
