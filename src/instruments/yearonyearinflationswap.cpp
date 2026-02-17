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
#include <ql/instruments/yearonyearinflationswap.hpp>
#include <ql/indexes/inflationindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::yearonyearinflationswap(py::module_& m) {
    // Note: YearOnYearInflationSwap::Type is Swap::Type (already registered
    // as SwapType). Use SwapType.Receiver / SwapType.Payer in Python.

    // YearOnYearInflationSwap
    py::class_<YearOnYearInflationSwap, Swap,
               ext::shared_ptr<YearOnYearInflationSwap>>(
        m, "YearOnYearInflationSwap",
        "Year-on-year inflation swap.")
        .def(py::init<YearOnYearInflationSwap::Type,
                       Real,
                       Schedule,
                       Rate,
                       DayCounter,
                       Schedule,
                       ext::shared_ptr<YoYInflationIndex>,
                       const Period&,
                       CPI::InterpolationType,
                       Spread,
                       DayCounter,
                       Calendar,
                       BusinessDayConvention>(),
            py::arg("type"),
            py::arg("nominal"),
            py::arg("fixedSchedule"),
            py::arg("fixedRate"),
            py::arg("fixedDayCount"),
            py::arg("yoySchedule"),
            py::arg("yoyIndex"),
            py::arg("observationLag"),
            py::arg("interpolation"),
            py::arg("spread"),
            py::arg("yoyDayCount"),
            py::arg("paymentCalendar"),
            py::arg("paymentConvention") = ModifiedFollowing,
            "Constructs a year-on-year inflation swap.")
        // Inspectors
        .def("type", &YearOnYearInflationSwap::type,
            "Returns the swap type.")
        .def("nominal", &YearOnYearInflationSwap::nominal,
            "Returns the nominal.")
        .def("fixedSchedule", &YearOnYearInflationSwap::fixedSchedule,
            py::return_value_policy::reference_internal,
            "Returns the fixed schedule.")
        .def("fixedRate", &YearOnYearInflationSwap::fixedRate,
            "Returns the fixed rate.")
        .def("fixedDayCount", &YearOnYearInflationSwap::fixedDayCount,
            py::return_value_policy::reference_internal,
            "Returns the fixed-leg day counter.")
        .def("yoySchedule", &YearOnYearInflationSwap::yoySchedule,
            py::return_value_policy::reference_internal,
            "Returns the YoY schedule.")
        .def("yoyInflationIndex",
            &YearOnYearInflationSwap::yoyInflationIndex,
            "Returns the YoY inflation index.")
        .def("observationLag",
            &YearOnYearInflationSwap::observationLag,
            "Returns the observation lag.")
        .def("spread", &YearOnYearInflationSwap::spread,
            "Returns the spread.")
        .def("yoyDayCount", &YearOnYearInflationSwap::yoyDayCount,
            py::return_value_policy::reference_internal,
            "Returns the YoY-leg day counter.")
        .def("paymentCalendar",
            &YearOnYearInflationSwap::paymentCalendar,
            "Returns the payment calendar.")
        .def("paymentConvention",
            &YearOnYearInflationSwap::paymentConvention,
            "Returns the payment convention.")
        .def("fixedLeg", &YearOnYearInflationSwap::fixedLeg,
            py::return_value_policy::reference_internal,
            "Returns the fixed leg.")
        .def("yoyLeg", &YearOnYearInflationSwap::yoyLeg,
            py::return_value_policy::reference_internal,
            "Returns the YoY leg.")
        // Results
        .def("fixedLegNPV", &YearOnYearInflationSwap::fixedLegNPV,
            "Returns the fixed-leg NPV.")
        .def("yoyLegNPV", &YearOnYearInflationSwap::yoyLegNPV,
            "Returns the YoY-leg NPV.")
        .def("fairRate", &YearOnYearInflationSwap::fairRate,
            "Returns the fair fixed rate.")
        .def("fairSpread", &YearOnYearInflationSwap::fairSpread,
            "Returns the fair spread.");
}
