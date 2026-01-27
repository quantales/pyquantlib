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
#include "pyquantlib/trampolines.h"
#include <ql/termstructures/volatility/smilesection.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::smilesection(py::module_& m) {
    py::class_<SmileSection, PySmileSection, ext::shared_ptr<SmileSection>,
               Observable, Observer>(
        m, "SmileSection",
        "Abstract base class for volatility smile sections.")
        .def(py::init_alias<>(),
            "Default constructor for Python subclassing.")
        .def(py::init_alias<Time, const DayCounter&, VolatilityType, Rate>(),
            py::arg("exerciseTime"),
            py::arg("dc"),
            py::arg("type"),
            py::arg("shift"),
            "Constructs with exercise time (all args required).")
        .def(py::init([](Time exerciseTime, const DayCounter& dc) {
            return new PySmileSection(exerciseTime, dc, ShiftedLognormal, 0.0);
        }),
            py::arg("exerciseTime"),
            py::arg("dc") = Actual365Fixed(),
            "Constructs with exercise time.")
        // SmileSection interface
        .def("minStrike", &SmileSection::minStrike,
            "Returns minimum strike.")
        .def("maxStrike", &SmileSection::maxStrike,
            "Returns maximum strike.")
        .def("atmLevel", &SmileSection::atmLevel,
            "Returns ATM level (forward).")
        .def("variance", &SmileSection::variance,
            py::arg("strike"),
            "Returns variance at the given strike.")
        .def("volatility",
            py::overload_cast<Rate>(&SmileSection::volatility, py::const_),
            py::arg("strike"),
            "Returns volatility at the given strike.")
        .def("volatility",
            py::overload_cast<Rate, VolatilityType, Real>(
                &SmileSection::volatility, py::const_),
            py::arg("strike"), py::arg("volatilityType"), py::arg("shift") = 0.0,
            "Returns volatility at the given strike with specified type.")
        .def("exerciseDate", &SmileSection::exerciseDate,
            py::return_value_policy::reference,
            "Returns the exercise date.")
        .def("exerciseTime", &SmileSection::exerciseTime,
            "Returns the time to exercise.")
        .def("dayCounter", &SmileSection::dayCounter,
            py::return_value_policy::reference,
            "Returns the day counter.")
        .def("referenceDate", &SmileSection::referenceDate,
            py::return_value_policy::reference,
            "Returns the reference date.")
        .def("volatilityType", &SmileSection::volatilityType,
            "Returns the volatility type.")
        .def("shift", &SmileSection::shift,
            "Returns the shift for shifted lognormal volatility.")
        .def("optionPrice", &SmileSection::optionPrice,
            py::arg("strike"),
            py::arg("type") = Option::Call,
            py::arg("discount") = 1.0,
            "Returns the option price at the given strike.")
        .def("digitalOptionPrice", &SmileSection::digitalOptionPrice,
            py::arg("strike"),
            py::arg("type") = Option::Call,
            py::arg("discount") = 1.0,
            py::arg("gap") = 1.0e-5,
            "Returns the digital option price at the given strike.")
        .def("vega", &SmileSection::vega,
            py::arg("strike"),
            py::arg("discount") = 1.0,
            "Returns the vega at the given strike.")
        .def("density", &SmileSection::density,
            py::arg("strike"),
            py::arg("discount") = 1.0,
            py::arg("gap") = 1.0e-4,
            "Returns the probability density at the given strike.");
}
