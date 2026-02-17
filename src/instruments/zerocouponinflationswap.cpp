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
#include <ql/instruments/zerocouponinflationswap.hpp>
#include <ql/indexes/inflationindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::zerocouponinflationswap(py::module_& m) {
    // Note: ZeroCouponInflationSwap::Type is Swap::Type (already registered
    // as SwapType). Use SwapType.Receiver / SwapType.Payer in Python.

    // ZeroCouponInflationSwap
    py::class_<ZeroCouponInflationSwap, Swap,
               ext::shared_ptr<ZeroCouponInflationSwap>>(
        m, "ZeroCouponInflationSwap",
        "Zero-coupon inflation swap.")
        .def(py::init([](ZeroCouponInflationSwap::Type type,
                         Real nominal,
                         const Date& startDate,
                         const Date& maturity,
                         Calendar fixCalendar,
                         BusinessDayConvention fixConvention,
                         DayCounter dayCounter,
                         Rate fixedRate,
                         const ext::shared_ptr<ZeroInflationIndex>& infIndex,
                         const Period& observationLag,
                         CPI::InterpolationType observationInterpolation,
                         bool adjustInfObsDates,
                         const py::object& infCalendar,
                         const py::object& infConvention) {
                Calendar ic;
                if (!infCalendar.is_none())
                    ic = infCalendar.cast<Calendar>();
                BusinessDayConvention ibc = BusinessDayConvention();
                if (!infConvention.is_none())
                    ibc = infConvention.cast<BusinessDayConvention>();
                return ext::make_shared<ZeroCouponInflationSwap>(
                    type, nominal, startDate, maturity,
                    std::move(fixCalendar), fixConvention,
                    std::move(dayCounter), fixedRate,
                    infIndex, observationLag, observationInterpolation,
                    adjustInfObsDates, std::move(ic), ibc);
            }),
            py::arg("type"),
            py::arg("nominal"),
            py::arg("startDate"),
            py::arg("maturity"),
            py::arg("fixCalendar"),
            py::arg("fixConvention"),
            py::arg("dayCounter"),
            py::arg("fixedRate"),
            py::arg("infIndex"),
            py::arg("observationLag"),
            py::arg("observationInterpolation"),
            py::arg("adjustInfObsDates") = false,
            py::arg("infCalendar") = py::none(),
            py::arg("infConvention") = py::none(),
            "Constructs a zero-coupon inflation swap.")
        // Inspectors
        .def("type", &ZeroCouponInflationSwap::type,
            "Returns the swap type.")
        .def("nominal", &ZeroCouponInflationSwap::nominal,
            "Returns the nominal.")
        .def("fixedCalendar", &ZeroCouponInflationSwap::fixedCalendar,
            "Returns the fixed-leg calendar.")
        .def("fixedConvention", &ZeroCouponInflationSwap::fixedConvention,
            "Returns the fixed-leg business day convention.")
        .def("dayCounter", &ZeroCouponInflationSwap::dayCounter,
            "Returns the day counter.")
        .def("fixedRate", &ZeroCouponInflationSwap::fixedRate,
            "Returns the fixed rate.")
        .def("inflationIndex", &ZeroCouponInflationSwap::inflationIndex,
            "Returns the inflation index.")
        .def("observationLag", &ZeroCouponInflationSwap::observationLag,
            "Returns the observation lag.")
        .def("observationInterpolation",
            &ZeroCouponInflationSwap::observationInterpolation,
            "Returns the observation interpolation type.")
        .def("adjustObservationDates",
            &ZeroCouponInflationSwap::adjustObservationDates,
            "Returns whether observation dates are adjusted.")
        .def("inflationCalendar",
            &ZeroCouponInflationSwap::inflationCalendar,
            "Returns the inflation calendar.")
        .def("inflationConvention",
            &ZeroCouponInflationSwap::inflationConvention,
            "Returns the inflation business day convention.")
        .def("fixedLeg", &ZeroCouponInflationSwap::fixedLeg,
            py::return_value_policy::reference_internal,
            "Returns the fixed leg.")
        .def("inflationLeg", &ZeroCouponInflationSwap::inflationLeg,
            py::return_value_policy::reference_internal,
            "Returns the inflation leg.")
        // Results
        .def("fixedLegNPV", &ZeroCouponInflationSwap::fixedLegNPV,
            "Returns the fixed leg NPV.")
        .def("inflationLegNPV",
            &ZeroCouponInflationSwap::inflationLegNPV,
            "Returns the inflation leg NPV.")
        .def("fairRate", &ZeroCouponInflationSwap::fairRate,
            "Returns the fair fixed rate.");
}
