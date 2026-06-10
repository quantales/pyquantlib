/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2026 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is Copyright (c) 2000-2026 The QuantLib Authors
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/instruments/multipleresetsswap.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/time/calendars/nullcalendar.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::multipleresetsswap(py::module_& m) {
    py::class_<MultipleResetsSwap, FixedVsFloatingSwap,
               ext::shared_ptr<MultipleResetsSwap>>(
        m, "MultipleResetsSwap",
        "Swap with a fixed leg and a multiple-resets (compounded or averaged) floating leg.")
        .def(py::init([](Swap::Type type, Real nominal,
                         const Schedule& fixedSchedule, Rate fixedRate,
                         const DayCounter& fixedDayCount, const Schedule& fullResetSchedule,
                         const ext::shared_ptr<IborIndex>& iborIndex, Size resetsPerCoupon,
                         Spread spread, RateAveraging::Type averagingMethod,
                         const py::object& paymentConvention, Integer paymentLag,
                         const Calendar& paymentCalendar) {
            ext::optional<BusinessDayConvention> pc = ext::nullopt;
            if (!paymentConvention.is_none())
                pc = paymentConvention.cast<BusinessDayConvention>();
            return ext::make_shared<MultipleResetsSwap>(
                type, nominal, fixedSchedule, fixedRate, fixedDayCount,
                fullResetSchedule, iborIndex, resetsPerCoupon, spread,
                averagingMethod, pc, paymentLag, paymentCalendar);
        }),
            py::arg("type"),
            py::arg("nominal"),
            py::arg("fixedSchedule"),
            py::arg("fixedRate"),
            py::arg("fixedDayCount"),
            py::arg("fullResetSchedule"),
            py::arg("iborIndex"),
            py::arg("resetsPerCoupon"),
            py::arg("spread") = 0.0,
            py::arg("averagingMethod") = RateAveraging::Compound,
            py::arg("paymentConvention") = py::none(),
            py::arg("paymentLag") = 0,
            py::arg("paymentCalendar") = NullCalendar(),
            "Constructs a multiple-resets swap.")
        .def("fullResetSchedule", &MultipleResetsSwap::fullResetSchedule,
            py::return_value_policy::reference_internal,
            "Returns the full schedule of reset dates.")
        .def("resetsPerCoupon", &MultipleResetsSwap::resetsPerCoupon,
            "Returns the number of index resets per floating coupon.")
        .def("averagingMethod", &MultipleResetsSwap::averagingMethod,
            "Returns the averaging method (Compound or Simple).");
}
