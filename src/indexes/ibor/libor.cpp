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
#include <ql/indexes/ibor/libor.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::libor(py::module_& m) {
    py::class_<Libor, IborIndex, ext::shared_ptr<Libor>>(
        m, "Libor",
        "ICE LIBOR index, with the joint-calendar date conventions.")
        // Without a forwarding term structure
        .def(py::init([](const std::string& familyName, const Period& tenor,
                         Natural settlementDays, const Currency& currency,
                         const Calendar& financialCenterCalendar,
                         const DayCounter& dayCounter) {
            return ext::make_shared<Libor>(familyName, tenor, settlementDays,
                                           currency, financialCenterCalendar,
                                           dayCounter);
        }),
             py::arg("familyName"),
             py::arg("tenor"),
             py::arg("settlementDays"),
             py::arg("currency"),
             py::arg("financialCenterCalendar"),
             py::arg("dayCounter"),
             "Constructs a LIBOR index without a forwarding term structure.")
        .def(py::init<const std::string&, const Period&, Natural, const Currency&,
                      const Calendar&, const DayCounter&,
                      const Handle<YieldTermStructure>&>(),
             py::arg("familyName"),
             py::arg("tenor"),
             py::arg("settlementDays"),
             py::arg("currency"),
             py::arg("financialCenterCalendar"),
             py::arg("dayCounter"),
             py::arg("h"),
             "Constructs a LIBOR index with a forwarding term structure handle.")
        // Hidden handle constructor
        .def(py::init([](const std::string& familyName, const Period& tenor,
                         Natural settlementDays, const Currency& currency,
                         const Calendar& financialCenterCalendar,
                         const DayCounter& dayCounter,
                         const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<Libor>(familyName, tenor, settlementDays,
                                           currency, financialCenterCalendar,
                                           dayCounter,
                                           Handle<YieldTermStructure>(ts));
        }),
             py::arg("familyName"),
             py::arg("tenor"),
             py::arg("settlementDays"),
             py::arg("currency"),
             py::arg("financialCenterCalendar"),
             py::arg("dayCounter"),
             py::arg("forwardingTermStructure"),
             "Constructs a LIBOR index (handle created internally).")
        .def("jointCalendar", &Libor::jointCalendar,
             "Returns the joint calendar of the index and financial centre.");

    py::class_<DailyTenorLibor, IborIndex, ext::shared_ptr<DailyTenorLibor>>(
        m, "DailyTenorLibor",
        "Overnight/one-day-deposit ICE LIBOR index.")
        // Without a forwarding term structure
        .def(py::init([](const std::string& familyName, Natural settlementDays,
                         const Currency& currency,
                         const Calendar& financialCenterCalendar,
                         const DayCounter& dayCounter) {
            return ext::make_shared<DailyTenorLibor>(
                familyName, settlementDays, currency, financialCenterCalendar,
                dayCounter);
        }),
             py::arg("familyName"),
             py::arg("settlementDays"),
             py::arg("currency"),
             py::arg("financialCenterCalendar"),
             py::arg("dayCounter"),
             "Constructs a daily-tenor LIBOR index without a term structure.")
        .def(py::init<const std::string&, Natural, const Currency&,
                      const Calendar&, const DayCounter&,
                      const Handle<YieldTermStructure>&>(),
             py::arg("familyName"),
             py::arg("settlementDays"),
             py::arg("currency"),
             py::arg("financialCenterCalendar"),
             py::arg("dayCounter"),
             py::arg("h"),
             "Constructs a daily-tenor LIBOR index with a forwarding handle.")
        .def(py::init([](const std::string& familyName, Natural settlementDays,
                         const Currency& currency,
                         const Calendar& financialCenterCalendar,
                         const DayCounter& dayCounter,
                         const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<DailyTenorLibor>(
                familyName, settlementDays, currency, financialCenterCalendar,
                dayCounter, Handle<YieldTermStructure>(ts));
        }),
             py::arg("familyName"),
             py::arg("settlementDays"),
             py::arg("currency"),
             py::arg("financialCenterCalendar"),
             py::arg("dayCounter"),
             py::arg("forwardingTermStructure"),
             "Constructs a daily-tenor LIBOR index (handle created internally).");
}
