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
#include <ql/indexes/iborindex.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::iborindex(py::module_& m) {
    // IborIndex class
    py::class_<IborIndex, InterestRateIndex, ext::shared_ptr<IborIndex>>(
        m, "IborIndex",
        "Base class for IBOR indexes (e.g. Euribor, Libor).")
        // Constructor without term structure
        .def(py::init([](const std::string& familyName, const Period& tenor,
                        Natural settlementDays, const Currency& currency,
                        const Calendar& fixingCalendar, BusinessDayConvention convention,
                        bool endOfMonth, const DayCounter& dayCounter) {
            return ext::make_shared<IborIndex>(
                familyName, tenor, settlementDays, currency, fixingCalendar,
                convention, endOfMonth, dayCounter);
        }),
            py::arg("familyName"),
            py::arg("tenor"),
            py::arg("settlementDays"),
            py::arg("currency"),
            py::arg("fixingCalendar"),
            py::arg("convention"),
            py::arg("endOfMonth"),
            py::arg("dayCounter"),
            "Constructs an IBOR index without forwarding curve.")
        // Constructor with handle
        .def(py::init<const std::string&, const Period&, Natural, const Currency&,
                      const Calendar&, BusinessDayConvention, bool, const DayCounter&,
                      Handle<YieldTermStructure>>(),
            py::arg("familyName"),
            py::arg("tenor"),
            py::arg("settlementDays"),
            py::arg("currency"),
            py::arg("fixingCalendar"),
            py::arg("convention"),
            py::arg("endOfMonth"),
            py::arg("dayCounter"),
            py::arg("h"),
            "Constructs an IBOR index with forwarding term structure handle.")
        // Hidden handle constructor
        .def(py::init([](const std::string& familyName, const Period& tenor,
                        Natural settlementDays, const Currency& currency,
                        const Calendar& fixingCalendar, BusinessDayConvention convention,
                        bool endOfMonth, const DayCounter& dayCounter,
                        const ext::shared_ptr<YieldTermStructure>& ts) {
            return ext::make_shared<IborIndex>(
                familyName, tenor, settlementDays, currency, fixingCalendar,
                convention, endOfMonth, dayCounter,
                Handle<YieldTermStructure>(ts));
        }),
            py::arg("familyName"),
            py::arg("tenor"),
            py::arg("settlementDays"),
            py::arg("currency"),
            py::arg("fixingCalendar"),
            py::arg("convention"),
            py::arg("endOfMonth"),
            py::arg("dayCounter"),
            py::arg("forwardingTermStructure"),
            "Constructs an IBOR index with forwarding term structure.")
        .def("businessDayConvention", &IborIndex::businessDayConvention,
            "Returns the business day convention.")
        .def("endOfMonth", &IborIndex::endOfMonth,
            "Returns True if end-of-month adjustment applies.")
        .def("forwardingTermStructure", &IborIndex::forwardingTermStructure,
            "Returns the forwarding term structure handle.")
        .def("clone", &IborIndex::clone,
            py::arg("forwardingTermStructure"),
            "Returns a copy linked to a different forwarding curve.");

    // OvernightIndex class
    py::class_<OvernightIndex, IborIndex, ext::shared_ptr<OvernightIndex>>(
        m, "OvernightIndex",
        "Base class for overnight indexes.")
        // Constructor without term structure
        .def(py::init([](const std::string& familyName, Natural settlementDays,
                        const Currency& currency, const Calendar& fixingCalendar,
                        const DayCounter& dayCounter) {
            return ext::make_shared<OvernightIndex>(
                familyName, settlementDays, currency, fixingCalendar, dayCounter);
        }),
            py::arg("familyName"),
            py::arg("settlementDays"),
            py::arg("currency"),
            py::arg("fixingCalendar"),
            py::arg("dayCounter"),
            "Constructs an overnight index without forwarding curve.")
        // Constructor with handle
        .def(py::init<const std::string&, Natural, const Currency&,
                      const Calendar&, const DayCounter&,
                      const Handle<YieldTermStructure>&>(),
            py::arg("familyName"),
            py::arg("settlementDays"),
            py::arg("currency"),
            py::arg("fixingCalendar"),
            py::arg("dayCounter"),
            py::arg("h"),
            "Constructs an overnight index with forwarding term structure handle.");
}
