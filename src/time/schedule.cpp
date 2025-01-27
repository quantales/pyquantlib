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
#include <ql/time/schedule.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_time::schedule(py::module_ &m) {

    py::class_<Schedule> pyClassSchedule(m, "Schedule",
        "Payment schedule for a financial instrument.");

    pyClassSchedule
        .def(py::init([](
            const std::vector<Date>& dates,
            Calendar calendar = NullCalendar(),
            BusinessDayConvention convention = Unadjusted,
            const ext::optional<BusinessDayConvention>& terminationDateConvention = ext::nullopt,
            const ext::optional<Period>& tenor = ext::nullopt,
            const ext::optional<DateGeneration::Rule>& rule = ext::nullopt,
            const ext::optional<bool>& endOfMonth = ext::nullopt,
            const std::vector<bool>& isRegular = std::vector<bool>{}) {
                return new Schedule(dates, calendar, convention, terminationDateConvention,
                                tenor, rule, endOfMonth, isRegular);
            }),
            py::arg("dates"),
            py::arg("calendar") = NullCalendar(),
            py::arg("convention") = Unadjusted,
            py::arg("terminationDateConvention") = ext::nullopt,
            py::arg("tenor") = ext::nullopt,
            py::arg("rule") = ext::nullopt,
            py::arg("endOfMonth") = ext::nullopt,
            py::arg("isRegular") = std::vector<bool>{}
        )
        .def(py::init<
            Date, const Date&, const Period&, Calendar,
            BusinessDayConvention, BusinessDayConvention,
            DateGeneration::Rule, bool,
            const Date&, const Date&
        >(),
            py::arg("effectiveDate"),
            py::arg("terminationDate"),
            py::arg("tenor"),
            py::arg("calendar"),
            py::arg("convention"),
            py::arg("terminationDateConvention"),
            py::arg("rule"),
            py::arg("endOfMonth"),
            py::arg("firstDate") = Date(),
            py::arg("nextToLastDate") = Date()
        )
        .def(py::init<>())
        ;

    // Size and indexing
    pyClassSchedule
        .def("__len__", &Schedule::size)
        .def("__getitem__", [](const Schedule &self, size_t i) {
            if (i >= self.size())
                throw py::index_error("Schedule index out of range");
            return self.date(i);
        }, py::is_operator())
        .def("at", &Schedule::at)
        .def("date", &Schedule::date)
        .def("dates", &Schedule::dates)
        .def("empty", &Schedule::empty)
        .def("front", &Schedule::front)
        .def("back", &Schedule::back)
        ;

    // Other inspectors
    pyClassSchedule
        .def("previousDate", &Schedule::previousDate)
        .def("nextDate", &Schedule::nextDate)
        .def("hasIsRegular", &Schedule::hasIsRegular)
        .def("isRegular", py::overload_cast<Size>(&Schedule::isRegular, py::const_))
        .def("isRegular", [](Schedule& self) { return self.isRegular(); })
        .def("calendar", &Schedule::calendar)
        .def("startDate", &Schedule::startDate)
        .def("endDate", &Schedule::endDate)
        .def("hasTenor", &Schedule::hasTenor)
        .def("tenor", &Schedule::tenor)
        .def("businessDayConvention", &Schedule::businessDayConvention)
        .def("hasTerminationDateBusinessDayConvention", &Schedule::hasTerminationDateBusinessDayConvention)
        .def("terminationDateBusinessDayConvention", &Schedule::terminationDateBusinessDayConvention)
        .def("hasRule", &Schedule::hasRule)
        .def("rule", &Schedule::rule)
        .def("hasEndOfMonth", &Schedule::hasEndOfMonth)
        .def("endOfMonth", &Schedule::endOfMonth)
        ;

    // Iterators
    pyClassSchedule
        .def("__iter__", [](const Schedule &self) {
            return py::make_iterator(self.begin(), self.end());
        }, py::keep_alive<0, 1>())
        .def("lower_bound", &Schedule::lower_bound, py::arg("date") = Date())
        ;

    // Utilities
    pyClassSchedule
        .def("after", &Schedule::after)
        .def("until", &Schedule::until)
        ;

    // MakeSchedule - fluent interface for building schedules
    py::class_<MakeSchedule>(m, "MakeSchedule",
        "Helper class providing a fluent interface for Schedule construction.")
        .def(py::init<>())
        .def("from_", &MakeSchedule::from,
            py::arg("effectiveDate"), py::return_value_policy::reference_internal)
        .def("to", &MakeSchedule::to,
            py::arg("terminationDate"), py::return_value_policy::reference_internal)
        .def("withTenor", &MakeSchedule::withTenor,
            py::arg("tenor"), py::return_value_policy::reference_internal)
        .def("withFrequency", &MakeSchedule::withFrequency,
            py::arg("frequency"), py::return_value_policy::reference_internal)
        .def("withCalendar", &MakeSchedule::withCalendar,
            py::arg("calendar"), py::return_value_policy::reference_internal)
        .def("withConvention", &MakeSchedule::withConvention,
            py::arg("convention"), py::return_value_policy::reference_internal)
        .def("withTerminationDateConvention", &MakeSchedule::withTerminationDateConvention,
            py::arg("terminationDateConvention"), py::return_value_policy::reference_internal)
        .def("withRule", &MakeSchedule::withRule,
            py::arg("rule"), py::return_value_policy::reference_internal)
        .def("forwards", &MakeSchedule::forwards,
            py::return_value_policy::reference_internal)
        .def("backwards", &MakeSchedule::backwards,
            py::return_value_policy::reference_internal)
        .def("endOfMonth", &MakeSchedule::endOfMonth,
            py::arg("flag") = true, py::return_value_policy::reference_internal)
        .def("withFirstDate", &MakeSchedule::withFirstDate,
            py::arg("d"), py::return_value_policy::reference_internal)
        .def("withNextToLastDate", &MakeSchedule::withNextToLastDate,
            py::arg("d"), py::return_value_policy::reference_internal)
        .def("schedule", &MakeSchedule::operator Schedule)
        ;

    py::implicitly_convertible<MakeSchedule, Schedule>();
}
