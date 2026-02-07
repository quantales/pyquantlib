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
#include <ql/indexes/swapindex.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/instruments/vanillaswap.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_indexes::swapindex(py::module_& m) {
    // SwapIndex
    py::class_<SwapIndex, InterestRateIndex, ext::shared_ptr<SwapIndex>>(
        m, "SwapIndex",
        "Swap rate index.")
        // Constructor without discounting curve
        .def(py::init<const std::string&, const Period&, Natural,
                      const Currency&, const Calendar&, const Period&,
                      BusinessDayConvention, const DayCounter&,
                      ext::shared_ptr<IborIndex>>(),
            py::arg("familyName"), py::arg("tenor"),
            py::arg("settlementDays"), py::arg("currency"),
            py::arg("fixingCalendar"), py::arg("fixedLegTenor"),
            py::arg("fixedLegConvention"), py::arg("fixedLegDayCounter"),
            py::arg("iborIndex"),
            "Constructs a swap index.")
        // Constructor with discounting curve handle
        .def(py::init<const std::string&, const Period&, Natural,
                      const Currency&, const Calendar&, const Period&,
                      BusinessDayConvention, const DayCounter&,
                      ext::shared_ptr<IborIndex>,
                      Handle<YieldTermStructure>>(),
            py::arg("familyName"), py::arg("tenor"),
            py::arg("settlementDays"), py::arg("currency"),
            py::arg("fixingCalendar"), py::arg("fixedLegTenor"),
            py::arg("fixedLegConvention"), py::arg("fixedLegDayCounter"),
            py::arg("iborIndex"), py::arg("discountingTermStructure"),
            "Constructs a swap index with discounting term structure.")
        // Hidden handle: shared_ptr overload for discounting curve
        .def(py::init([](const std::string& familyName, const Period& tenor,
                         Natural settlementDays, const Currency& currency,
                         const Calendar& fixingCalendar, const Period& fixedLegTenor,
                         BusinessDayConvention fixedLegConvention,
                         const DayCounter& fixedLegDayCounter,
                         const ext::shared_ptr<IborIndex>& iborIndex,
                         const ext::shared_ptr<YieldTermStructure>& disc) {
            return ext::make_shared<SwapIndex>(
                familyName, tenor, settlementDays, currency, fixingCalendar,
                fixedLegTenor, fixedLegConvention, fixedLegDayCounter,
                iborIndex, Handle<YieldTermStructure>(disc));
        }),
            py::arg("familyName"), py::arg("tenor"),
            py::arg("settlementDays"), py::arg("currency"),
            py::arg("fixingCalendar"), py::arg("fixedLegTenor"),
            py::arg("fixedLegConvention"), py::arg("fixedLegDayCounter"),
            py::arg("iborIndex"), py::arg("discountCurve"),
            "Constructs a swap index with discounting curve.")
        .def("fixedLegTenor", &SwapIndex::fixedLegTenor,
             py::return_value_policy::reference_internal,
             "Returns the fixed leg tenor.")
        .def("fixedLegConvention", &SwapIndex::fixedLegConvention,
             "Returns the fixed leg business day convention.")
        .def("iborIndex", &SwapIndex::iborIndex,
             "Returns the IBOR index.")
        .def("forwardingTermStructure", &SwapIndex::forwardingTermStructure,
             "Returns the forwarding term structure handle.")
        .def("discountingTermStructure", &SwapIndex::discountingTermStructure,
             "Returns the discounting term structure handle.")
        .def("exogenousDiscount", &SwapIndex::exogenousDiscount,
             "Returns true if using exogenous discounting.")
        .def("underlyingSwap", [](const SwapIndex& self, const Date& fixingDate)
                 -> py::object {
                 return py::cast(self.underlyingSwap(fixingDate));
             },
             py::arg("fixingDate"),
             "Returns the underlying swap for a given fixing date.");

    // OvernightIndexedSwapIndex
    py::class_<OvernightIndexedSwapIndex, SwapIndex,
               ext::shared_ptr<OvernightIndexedSwapIndex>>(
        m, "OvernightIndexedSwapIndex",
        "OIS swap rate index.")
        .def(py::init<const std::string&, const Period&, Natural,
                      const Currency&,
                      ext::shared_ptr<OvernightIndex>,
                      bool, RateAveraging::Type>(),
            py::arg("familyName"), py::arg("tenor"),
            py::arg("settlementDays"), py::arg("currency"),
            py::arg("overnightIndex"),
            py::arg("telescopicValueDates") = false,
            py::arg("averagingMethod") = RateAveraging::Compound,
            "Constructs an OIS swap rate index.")
        .def("overnightIndex", [](const OvernightIndexedSwapIndex& self)
                 -> py::object {
                 return py::cast(self.overnightIndex());
             },
             "Returns the overnight index.");
}
