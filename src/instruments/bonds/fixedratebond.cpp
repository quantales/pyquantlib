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
#include <ql/instruments/bonds/fixedratebond.hpp>
#include <ql/time/schedule.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::fixedratebond(py::module_& m) {
    py::class_<FixedRateBond, Bond, ext::shared_ptr<FixedRateBond>>(
        m, "FixedRateBond",
        "Fixed rate bond.")
        .def(py::init([](Natural settlementDays, Real faceAmount,
                         Schedule schedule,
                         const std::vector<Rate>& coupons,
                         const DayCounter& accrualDayCounter,
                         BusinessDayConvention paymentConvention,
                         Real redemption, const Date& issueDate,
                         const py::object& paymentCalendar,
                         const Period& exCouponPeriod,
                         const py::object& exCouponCalendar,
                         BusinessDayConvention exCouponConvention,
                         bool exCouponEndOfMonth,
                         const py::object& firstPeriodDayCounter) {
            Calendar payCal;
            if (!paymentCalendar.is_none())
                payCal = paymentCalendar.cast<Calendar>();
            Calendar exCal;
            if (!exCouponCalendar.is_none())
                exCal = exCouponCalendar.cast<Calendar>();
            DayCounter fpdc;
            if (!firstPeriodDayCounter.is_none())
                fpdc = firstPeriodDayCounter.cast<DayCounter>();
            return ext::make_shared<FixedRateBond>(
                settlementDays, faceAmount, std::move(schedule), coupons,
                accrualDayCounter, paymentConvention, redemption,
                issueDate, payCal, exCouponPeriod, exCal,
                exCouponConvention, exCouponEndOfMonth, fpdc);
        }),
            py::arg("settlementDays"),
            py::arg("faceAmount"),
            py::arg("schedule"),
            py::arg("coupons"),
            py::arg("accrualDayCounter"),
            py::arg("paymentConvention") = Following,
            py::arg("redemption") = 100.0,
            py::arg("issueDate") = Date(),
            py::arg("paymentCalendar") = py::none(),
            py::arg("exCouponPeriod") = Period(),
            py::arg("exCouponCalendar") = py::none(),
            py::arg("exCouponConvention") = Unadjusted,
            py::arg("exCouponEndOfMonth") = false,
            py::arg("firstPeriodDayCounter") = py::none(),
            "Constructs a fixed rate bond.")
        .def("frequency", &FixedRateBond::frequency,
            "Returns the coupon frequency.")
        .def("dayCounter", &FixedRateBond::dayCounter,
            py::return_value_policy::reference_internal,
            "Returns the accrual day counter.");
}
