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
#include <ql/quantlib.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

namespace py = pybind11;
using namespace QuantLib;

PYBIND11_MAKE_OPAQUE(std::vector<Calendar>);

void ql_time::calendarvector(py::module_& m)
{
    py::bind_vector<std::vector<Calendar>>(m, "CalendarVector",
        "A vector of Calendar objects, exposed as a Python list.")
        .def(py::init<>())  // default constructor (empty vector)
        .def(py::init<size_t>(), py::arg("size")); // add size constructor
}

void ql_time::calendar(py::module_& m)
{
    py::class_<QuantLib::Calendar, ext::shared_ptr<QuantLib::Calendar>>(m, "Calendar",
        "Calendar class for determining business days and holidays for a given market.")
        .def(py::init<>())
        .def("empty", &QuantLib::Calendar::empty,
            "Returns whether or not the calendar is initialized.")
        .def("name", &QuantLib::Calendar::name,
            "Returns the name of the calendar.")
        .def("addedHolidays", &QuantLib::Calendar::addedHolidays,
            "Returns the set of added holidays for the given calendar.")
        .def("removedHolidays", &QuantLib::Calendar::removedHolidays,
            "Returns the set of removed holidays for the given calendar.")
        .def("resetAddedAndRemovedHolidays", &QuantLib::Calendar::resetAddedAndRemovedHolidays,
            "Clear the set of added and removed holidays.")
        .def("isBusinessDay", &QuantLib::Calendar::isBusinessDay,
            py::arg("d"),
            "Returns True if the date is a business day.")
        .def("isHoliday", &QuantLib::Calendar::isHoliday,
            py::arg("d"),
            "Returns True if the date is a holiday.")
        .def("isWeekend", &QuantLib::Calendar::isWeekend,
            py::arg("w"),
            "Returns True if the weekday is part of the weekend.")
        .def("isStartOfMonth", &QuantLib::Calendar::isStartOfMonth,
            py::arg("d"),
            "Returns True if the date is on or before the first business day of its month.")
        .def("startOfMonth", &QuantLib::Calendar::startOfMonth,
            py::arg("d"),
            "First business day of the month to which the given date belongs.")
        .def("isEndOfMonth", &QuantLib::Calendar::isEndOfMonth,
            py::arg("d"),
            "Returns True if the date is on or after the last business day of its month.")
        .def("endOfMonth", &QuantLib::Calendar::endOfMonth,
            py::arg("d"),
            "Last business day of the month to which the given date belongs.")
        .def("addHoliday", &QuantLib::Calendar::addHoliday,
            py::arg("d"),
            "Adds a date to the set of holidays for the given calendar.")
        .def("removeHoliday", &QuantLib::Calendar::removeHoliday,
            py::arg("d"),
            "Removes a date from the set of holidays for the given calendar.")
        .def("holidayList", &QuantLib::Calendar::holidayList,
            py::arg("from_"), py::arg("to"), py::arg("includeWeekEnds") = false,
            "Returns the holidays between two dates.")
        .def("businessDayList", &QuantLib::Calendar::businessDayList,
            py::arg("from_"), py::arg("to"),
            "Returns the business days between two dates.")
        .def("adjust", &QuantLib::Calendar::adjust,
            py::arg("d"), py::arg("convention") = Following,
            "Adjusts a non-business day to the appropriate nearby business day.")
        .def("advance",
            py::overload_cast<const Date &, Integer, TimeUnit, BusinessDayConvention, bool>(&QuantLib::Calendar::advance, py::const_),
            py::arg("d"), py::arg("n"), py::arg("unit"), py::arg("convention") = Following, py::arg("endOfMonth") = false,
            "Advances the date by the given number of time units.")
        .def("advance",
            py::overload_cast<const Date &, const Period &, BusinessDayConvention, bool>(&QuantLib::Calendar::advance, py::const_),
            py::arg("d"), py::arg("period"), py::arg("convention") = Following, py::arg("endOfMonth") = false,
            "Advances the date by the given period.")
        .def("businessDaysBetween", &QuantLib::Calendar::businessDaysBetween,
            py::arg("from_"), py::arg("to"), py::arg("includeFirst") = true, py::arg("includeLast") = false,
            "Calculates the number of business days between two dates.")

        .def(py::self == py::self)
        .def(py::self != py::self)

        .def("__str__", [](const QuantLib::Calendar& cal) {
            std::ostringstream oss;
            oss << cal;
            return oss.str();
        })
        .def("__hash__", [](const QuantLib::Calendar& cal) {
            return cal.empty() ? 0 : std::hash<std::string>()(cal.name());
        })
        ;
}