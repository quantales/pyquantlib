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
#include <ql/instruments/bonds/amortizingfixedratebond.hpp>
#include <ql/time/schedule.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::amortizingfixedratebond(py::module_& m) {
    py::class_<AmortizingFixedRateBond, Bond,
               ext::shared_ptr<AmortizingFixedRateBond>>(
        m, "AmortizingFixedRateBond",
        "Amortizing fixed-rate bond.")
        .def(py::init([](Natural settlementDays,
                         const std::vector<Real>& notionals,
                         Schedule schedule,
                         const std::vector<Rate>& coupons,
                         const DayCounter& accrualDayCounter,
                         BusinessDayConvention paymentConvention,
                         const Date& issueDate,
                         const Period& exCouponPeriod,
                         const py::object& exCouponCalendar,
                         BusinessDayConvention exCouponConvention,
                         bool exCouponEndOfMonth,
                         const std::vector<Real>& redemptions,
                         Integer paymentLag) {
            Calendar exCal;
            if (!exCouponCalendar.is_none())
                exCal = exCouponCalendar.cast<Calendar>();
            return ext::make_shared<AmortizingFixedRateBond>(
                settlementDays, notionals, std::move(schedule), coupons,
                accrualDayCounter, paymentConvention, issueDate,
                exCouponPeriod, exCal, exCouponConvention,
                exCouponEndOfMonth, redemptions, paymentLag);
        }),
            py::arg("settlementDays"),
            py::arg("notionals"),
            py::arg("schedule"),
            py::arg("coupons"),
            py::arg("accrualDayCounter"),
            py::arg("paymentConvention") = Following,
            py::arg("issueDate") = Date(),
            py::arg("exCouponPeriod") = Period(),
            py::arg("exCouponCalendar") = py::none(),
            py::arg("exCouponConvention") = Unadjusted,
            py::arg("exCouponEndOfMonth") = false,
            py::arg("redemptions") = std::vector<Real>{100.0},
            py::arg("paymentLag") = 0,
            "Constructs an amortizing fixed-rate bond.")
        .def("frequency", &AmortizingFixedRateBond::frequency,
            "Returns the coupon frequency.")
        .def("dayCounter", &AmortizingFixedRateBond::dayCounter,
            py::return_value_policy::reference_internal,
            "Returns the accrual day counter.");

    m.def("sinkingSchedule", &sinkingSchedule,
        py::arg("startDate"), py::arg("bondLength"),
        py::arg("frequency"), py::arg("paymentCalendar"),
        "Returns a schedule for French amortization.");

    m.def("sinkingNotionals", &sinkingNotionals,
        py::arg("bondLength"), py::arg("frequency"),
        py::arg("couponRate"), py::arg("initialNotional"),
        "Returns notionals for French amortization.");
}
