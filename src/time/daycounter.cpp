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
#include <ql/time/daycounter.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_time::daycounter(py::module_& m)
{
    py::class_<DayCounter, ext::shared_ptr<QuantLib::DayCounter>>(m, "DayCounter",
        "Day counter base class, providing methods for time period calculations according to market conventions."
    )
    .def(py::init<>(), "Default (null) day counter constructor.")

    .def("empty", &DayCounter::empty, "Returns True if the day counter is not initialized.")
    .def("name", &DayCounter::name, "Returns the name of the day counter.")

    .def("dayCount",
         &DayCounter::dayCount,
         py::arg("d1"),
         py::arg("d2"),
         "Returns the number of days between two dates.")

    .def("yearFraction",
         &DayCounter::yearFraction,
         py::arg("d1"),
         py::arg("d2"),
         py::arg("refPeriodStart") = Date(),
         py::arg("refPeriodEnd") = Date(),
         "Returns the period between two dates as a fraction of year.")

    .def(py::self == py::self)
    .def(py::self != py::self)

    .def("__str__", [](const DayCounter& self) {
        return self.name();
    })
    .def("__repr__", [](const DayCounter& self) {
        std::ostringstream oss;
        oss << "<DayCounter: " << self.name() << ">";
        return oss.str();
    })
    .def("__hash__", [](const DayCounter& self) {
        return self.empty() ? 0 : std::hash<std::string>()(self.name());
    })
    ;
}
