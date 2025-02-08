/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 * 
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 * 
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#include "pyquantlib/pyquantlib.h"
#include "pyquantlib/trampolines.h"
#include <ql/termstructure.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_core::termstructure(py::module_& m) {
    py::class_<TermStructure, PyTermStructure, ext::shared_ptr<TermStructure>,
               Observer, Observable>(m, "TermStructure",
        "Abstract base class for term structures.")
        .def(py::init<DayCounter>(),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with day counter (defaults to Actual365Fixed).")
        .def(py::init<const Date&, const Calendar&, const DayCounter&>(),
            py::arg("referenceDate"), py::arg("calendar") = Calendar(),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with reference date, calendar, and day counter.")
        .def(py::init<Natural, const Calendar&, const DayCounter&>(),
            py::arg("settlementDays"), py::arg("calendar"),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with settlement days, calendar, and day counter.")
        .def("dayCounter", &TermStructure::dayCounter,
            "Returns the day counter.")
        .def("timeFromReference", &TermStructure::timeFromReference,
            py::arg("date"),
            "Returns the time from the reference date to the given date.")
        .def("maxDate", &TermStructure::maxDate,
            "Returns the latest date for which the curve can return values.")
        .def("maxTime", &TermStructure::maxTime,
            "Returns the latest time for which the curve can return values.")
        .def("referenceDate", &TermStructure::referenceDate,
            "Returns the reference date for the term structure.")
        .def("calendar", &TermStructure::calendar,
            "Returns the calendar.")
        .def("settlementDays", &TermStructure::settlementDays,
            "Returns the number of settlement days.");
}
