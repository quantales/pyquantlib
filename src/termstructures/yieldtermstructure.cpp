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
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/time/daycounters/actual365fixed.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_termstructures::yieldtermstructure(py::module_& m) {
    py::class_<YieldTermStructure, PyYieldTermStructure,
               ext::shared_ptr<YieldTermStructure>, TermStructure>(
        m, "YieldTermStructure",
        "Abstract base class for yield term structures.")
        .def(py::init<const DayCounter&>(),
            py::arg("dayCounter") = Actual365Fixed(),
            "Constructs with day counter (defaults to Actual365Fixed).")
        .def(py::init<const Date&, const Calendar&, const DayCounter&,
                      std::vector<Handle<Quote>>, const std::vector<Date>&>(),
            py::arg("referenceDate"),
            py::arg("calendar") = Calendar(),
            py::arg("dayCounter") = Actual365Fixed(),
            py::arg("jumps") = std::vector<Handle<Quote>>{},
            py::arg("jumpDates") = std::vector<Date>{},
            "Constructs with reference date, calendar, day counter, and optional jumps.")
        .def(py::init<Natural, const Calendar&, const DayCounter&,
                      std::vector<Handle<Quote>>, const std::vector<Date>&>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("dayCounter") = Actual365Fixed(),
            py::arg("jumps") = std::vector<Handle<Quote>>{},
            py::arg("jumpDates") = std::vector<Date>{},
            "Constructs with settlement days, calendar, day counter, and optional jumps.")
        // Discount factor methods
        .def("discount",
            py::overload_cast<const Date&, bool>(&YieldTermStructure::discount, py::const_),
            py::arg("date"), py::arg("extrapolate") = false,
            "Returns the discount factor for the given date.")
        .def("discount",
            py::overload_cast<Time, bool>(&YieldTermStructure::discount, py::const_),
            py::arg("time"), py::arg("extrapolate") = false,
            "Returns the discount factor for the given time.")
        // Zero rate methods
        .def("zeroRate",
            py::overload_cast<const Date&, const DayCounter&, Compounding, Frequency, bool>(
                &YieldTermStructure::zeroRate, py::const_),
            py::arg("date"), py::arg("dayCounter"), py::arg("compounding"),
            py::arg("frequency") = Annual, py::arg("extrapolate") = false,
            "Returns the zero rate for the given date.")
        .def("zeroRate",
            py::overload_cast<Time, Compounding, Frequency, bool>(
                &YieldTermStructure::zeroRate, py::const_),
            py::arg("time"), py::arg("compounding"),
            py::arg("frequency") = Annual, py::arg("extrapolate") = false,
            "Returns the zero rate for the given time.")
        // Forward rate methods
        .def("forwardRate",
            py::overload_cast<const Date&, const Date&, const DayCounter&,
                              Compounding, Frequency, bool>(
                &YieldTermStructure::forwardRate, py::const_),
            py::arg("date1"), py::arg("date2"), py::arg("dayCounter"),
            py::arg("compounding"), py::arg("frequency") = Annual,
            py::arg("extrapolate") = false,
            "Returns the forward rate between two dates.")
        .def("forwardRate",
            py::overload_cast<const Date&, const Period&, const DayCounter&,
                              Compounding, Frequency, bool>(
                &YieldTermStructure::forwardRate, py::const_),
            py::arg("date"), py::arg("period"), py::arg("dayCounter"),
            py::arg("compounding"), py::arg("frequency") = Annual,
            py::arg("extrapolate") = false,
            "Returns the forward rate for a date and period.")
        .def("forwardRate",
            py::overload_cast<Time, Time, Compounding, Frequency, bool>(
                &YieldTermStructure::forwardRate, py::const_),
            py::arg("time1"), py::arg("time2"), py::arg("compounding"),
            py::arg("frequency") = Annual, py::arg("extrapolate") = false,
            "Returns the forward rate between two times.")
        // Jump methods
        .def("jumpDates", &YieldTermStructure::jumpDates,
            "Returns the jump dates.")
        .def("jumpTimes", &YieldTermStructure::jumpTimes,
            "Returns the jump times.")
        .def("update", &YieldTermStructure::update,
            "Notifies observers of a change.");
}

void ql_termstructures::yieldtermstructurehandle(py::module_& m) {
    bindHandle<YieldTermStructure>(m, "YieldTermStructureHandle",
        "Handle to YieldTermStructure.");
}

void ql_termstructures::relinkableyieldtermstructurehandle(py::module_& m) {
    bindRelinkableHandle<YieldTermStructure>(m, "RelinkableYieldTermStructureHandle",
        "Relinkable handle to YieldTermStructure.");
}
