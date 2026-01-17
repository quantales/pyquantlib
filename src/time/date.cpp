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
#include <ql/time/date.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_time::date(py::module_& m)
{
    py::enum_<QuantLib::Month>(m, "Month", py::arithmetic(), "Month names enumeration.")
    .value("January", QuantLib::January)
    .value("February", QuantLib::February)
    .value("March", QuantLib::March)
    .value("April", QuantLib::April)
    .value("May", QuantLib::May)
    .value("June", QuantLib::June)
    .value("July", QuantLib::July)
    .value("August", QuantLib::August)
    .value("September", QuantLib::September)
    .value("October", QuantLib::October)
    .value("November", QuantLib::November)
    .value("December", QuantLib::December)
    .value("Jan", QuantLib::Jan)
    .value("Feb", QuantLib::Feb)
    .value("Mar", QuantLib::Mar)
    .value("Apr", QuantLib::Apr)
    .value("Jun", QuantLib::Jun)
    .value("Jul", QuantLib::Jul)
    .value("Aug", QuantLib::Aug)
    .value("Sep", QuantLib::Sep)
    .value("Oct", QuantLib::Oct)
    .value("Nov", QuantLib::Nov)
    .value("Dec", QuantLib::Dec)
    .export_values()

    // Mod-12 arithmetic: ensures intuitive cyclic behavior & avoids undefined values
    .def("__add__", [](Month m, int n) {
        int base = static_cast<int>(m) - 1;
        return static_cast<Month>((base + n) % 12 + 1);
    })
    .def("__radd__", [](int n, Month m) {
        int base = static_cast<int>(m) - 1;
        return static_cast<Month>((n + base) % 12 + 1);
    })
    .def("__sub__", [](Month m, int n) {
        int base = static_cast<int>(m) - 1;
        return static_cast<Month>((base - n + 12) % 12 + 1);
    })
    .def("__rsub__", [](int n, Month m) {
        int base = static_cast<int>(m) - 1;
        return static_cast<Month>((n - base + 12) % 12 + 1);
    });

    py::implicitly_convertible<int, Month>();

    py::class_<QuantLib::Date>(m, "Date", "Date class for date algebra and calendar operations.")
    .def(py::init<>(), "Default constructor returning a null date.")
    .def(py::init<Date::serial_type>(),
        py::arg("serialNumber"),
        "Constructor taking a serial number as given by Excel.")
    .def(py::init<Day, QuantLib::Month, Year>(),
        py::arg("d"), py::arg("m"), py::arg("y"),
        "Constructor taking day, month, year.")
    .def("weekday", &QuantLib::Date::weekday)
    .def("dayOfMonth", &QuantLib::Date::dayOfMonth)
    .def("dayOfYear", &QuantLib::Date::dayOfYear)
    .def("month", &QuantLib::Date::month)
    .def("year", &QuantLib::Date::year)
    .def("serialNumber", &QuantLib::Date::serialNumber)
    .def("__iadd__",
        py::overload_cast<Date::serial_type>(&QuantLib::Date::operator+=),
        py::arg("days"),
        "Increment date by the given number of days.")
    .def("__iadd__",
        py::overload_cast<const Period &>(&QuantLib::Date::operator+=),
        py::arg("period"),
        "Increment date by the given period.")
    .def("__isub__",
        py::overload_cast<Date::serial_type>(&QuantLib::Date::operator-=),
        py::arg("days"),
        "Decrement date by the given number of days.")
    .def("__isub__",
        py::overload_cast<const Period &>(&QuantLib::Date::operator-=),
        py::arg("period"),
        "Decrement date by the given period.")
    .def("__add__",
        py::overload_cast<Date::serial_type>(&QuantLib::Date::operator+, py::const_),
        py::arg("days"),
        "Return a new date incremented by the given number of days.")
    .def("__add__",
        py::overload_cast<const Period &>(&QuantLib::Date::operator+, py::const_),
        py::arg("period"),
        "Return a new date incremented by the given period.")
    .def("__sub__",
        py::overload_cast<Date::serial_type>(&QuantLib::Date::operator-, py::const_),
        py::arg("days"),
        "Return a new date decremented by the given number of days.")
    .def("__sub__",
        py::overload_cast<const Period &>(&QuantLib::Date::operator-, py::const_),
        py::arg("period"),
        "Return a new date decremented by the given period.")
    .def_static("todaysDate", &QuantLib::Date::todaysDate, "Today's date.")
    .def_static("minDate", &QuantLib::Date::minDate, "Earliest allowed date.")
    .def_static("maxDate", &QuantLib::Date::maxDate, "Latest allowed date.")
    .def_static("isLeap", &QuantLib::Date::isLeap,
        py::arg("y"),
        "Whether the given year is a leap one.")
    .def_static("startOfMonth", &QuantLib::Date::startOfMonth,
        py::arg("d"),
        "First day of the month to which the given date belongs.")
    .def_static("isStartOfMonth", &QuantLib::Date::isStartOfMonth,
        py::arg("d"),
        "Whether a date is the first day of its month.")
    .def_static("endOfMonth", &QuantLib::Date::endOfMonth,
        py::arg("d"),
        "Last day of the month to which the given date belongs.")
    .def_static("isEndOfMonth", &QuantLib::Date::isEndOfMonth,
        py::arg("d"),
        "Whether a date is the last day of its month.")
    .def_static("nextWeekday", &QuantLib::Date::nextWeekday,
        py::arg("d"), py::arg("w"),
        "Next given weekday following the given date.")
    .def_static("nthWeekday", &QuantLib::Date::nthWeekday,
        py::arg("n"), py::arg("w"), py::arg("m"), py::arg("y"),
        "The n-th given weekday in the given month and year.")

    .def("__str__", [](const QuantLib::Date& d) {
            std::ostringstream oss;
            oss << d;
            return oss.str();
        })

    .def("__repr__", [](const QuantLib::Date& d) {
            std::ostringstream oss;
            oss << "<Date: " << d << ">";
            return oss.str();
        })

    .def("__hash__", [](const QuantLib::Date& d) {
        return QuantLib::hash_value(d);
    })

    .def(py::self == py::self)
    .def(py::self != py::self)
    .def(py::self < py::self)
    .def(py::self <= py::self)
    .def(py::self > py::self)
    .def(py::self >= py::self)

    .def("to_date", [](const Date& d) {
        return py::module_::import("datetime").attr("date")(d.year(), d.month(), d.dayOfMonth());
    })
    .def_static("from_date", [](const py::object& dt) -> Date {
        if (py::hasattr(dt, "year") && py::hasattr(dt, "month") && py::hasattr(dt, "day")) {
            int y = py::int_(dt.attr("year"));
            int m = py::int_(dt.attr("month"));
            int d = py::int_(dt.attr("day"));
            return Date(d, Month(m), y);
        }
        throw std::runtime_error("from_date requires a date");
    })


    // Automatic conversion from Python datetime.date (or datetime.datetime) to QuantLib::Date
    // e.g.: ql.Date(datetime.date(2025, 1, 20))
    // or    ql.Date(datetime.datetime(2025, 1, 20))

    .def(py::init([](py::object obj) {
        // Accept both datetime.date and datetime.datetime
        if (py::hasattr(obj, "year") && py::hasattr(obj, "month") && py::hasattr(obj, "day")) {
            int y = obj.attr("year").cast<int>();
            int m = obj.attr("month").cast<int>();
            int d = obj.attr("day").cast<int>();
            return QuantLib::Date(d, static_cast<Month>(m), y);
        } else {
            throw std::runtime_error("Cannot convert object to QuantLib::Date. Expected datetime.date or datetime.datetime.");
        }
    }))
    ;

    m.def("daysBetween", QuantLib::daysBetween,
        py::arg("d1"), py::arg("d2"),
        "Difference in days (including fraction) between dates.");

    // Enable implicit conversion from Python datetime.date/datetime to QuantLib::Date
    // This allows passing datetime objects directly to functions expecting Date
    py::implicitly_convertible<py::object, QuantLib::Date>();
}