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
#include <ql/instruments/overnightindexedswap.hpp>
#include <ql/indexes/iborindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::overnightindexedswap(py::module_& m) {
    py::class_<OvernightIndexedSwap, FixedVsFloatingSwap,
               ext::shared_ptr<OvernightIndexedSwap>>(
        m, "OvernightIndexedSwap",
        "Overnight indexed swap: fixed vs overnight floating leg.")
        // Single nominal, single schedule constructor
        .def(py::init([](Swap::Type type, Real nominal,
                         const Schedule& schedule,
                         Rate fixedRate, const DayCounter& fixedDC,
                         const ext::shared_ptr<OvernightIndex>& overnightIndex,
                         Spread spread, Integer paymentLag,
                         BusinessDayConvention paymentAdjustment,
                         bool telescopicValueDates,
                         RateAveraging::Type averagingMethod) {
            return ext::make_shared<OvernightIndexedSwap>(
                type, nominal, schedule, fixedRate, fixedDC, overnightIndex,
                spread, paymentLag, paymentAdjustment, Calendar(),
                telescopicValueDates, averagingMethod);
        }),
            py::arg("type"), py::arg("nominal"),
            py::arg("schedule"),
            py::arg("fixedRate"), py::arg("fixedDC"),
            py::arg("overnightIndex"),
            py::arg("spread") = 0.0,
            py::arg("paymentLag") = 0,
            py::arg("paymentAdjustment") = Following,
            py::arg("telescopicValueDates") = false,
            py::arg("averagingMethod") = RateAveraging::Compound,
            "Constructs an overnight indexed swap.")
        // Separate fixed/overnight schedules constructor
        .def(py::init([](Swap::Type type, Real nominal,
                         const Schedule& fixedSchedule,
                         Rate fixedRate, const DayCounter& fixedDC,
                         const Schedule& overnightSchedule,
                         const ext::shared_ptr<OvernightIndex>& overnightIndex,
                         Spread spread, Integer paymentLag,
                         BusinessDayConvention paymentAdjustment,
                         bool telescopicValueDates,
                         RateAveraging::Type averagingMethod) {
            return ext::make_shared<OvernightIndexedSwap>(
                type, nominal, fixedSchedule, fixedRate, fixedDC,
                overnightSchedule, overnightIndex,
                spread, paymentLag, paymentAdjustment, Calendar(),
                telescopicValueDates, averagingMethod);
        }),
            py::arg("type"), py::arg("nominal"),
            py::arg("fixedSchedule"),
            py::arg("fixedRate"), py::arg("fixedDC"),
            py::arg("overnightSchedule"),
            py::arg("overnightIndex"),
            py::arg("spread") = 0.0,
            py::arg("paymentLag") = 0,
            py::arg("paymentAdjustment") = Following,
            py::arg("telescopicValueDates") = false,
            py::arg("averagingMethod") = RateAveraging::Compound,
            "Constructs an OIS with separate fixed and overnight schedules.")
        .def("overnightIndex", [](const OvernightIndexedSwap& self)
                 -> py::object {
                 return py::cast(self.overnightIndex());
             },
             "Returns the overnight index.")
        .def("overnightLeg", &OvernightIndexedSwap::overnightLeg,
             py::return_value_policy::reference_internal,
             "Returns the overnight leg cash flows.")
        .def("averagingMethod", &OvernightIndexedSwap::averagingMethod,
             "Returns the rate averaging method.")
        .def("overnightLegBPS", &OvernightIndexedSwap::overnightLegBPS,
             "Returns the BPS of the overnight leg.")
        .def("overnightLegNPV", &OvernightIndexedSwap::overnightLegNPV,
             "Returns the NPV of the overnight leg.");
}
