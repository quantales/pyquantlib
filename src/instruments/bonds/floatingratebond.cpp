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
#include <ql/instruments/bonds/floatingratebond.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/time/daycounter.hpp>
#include <ql/time/schedule.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::floatingratebond(py::module_& m) {
    py::class_<FloatingRateBond, Bond, ext::shared_ptr<FloatingRateBond>>(
        m, "FloatingRateBond",
        "Floating rate bond.")
        .def(py::init([](Natural settlementDays, Real faceAmount,
                         Schedule schedule,
                         const ext::shared_ptr<IborIndex>& iborIndex,
                         const DayCounter& accrualDayCounter,
                         BusinessDayConvention paymentConvention,
                         const py::object& fixingDays,
                         const std::vector<Real>& gearings,
                         const std::vector<Spread>& spreads,
                         const std::vector<Rate>& caps,
                         const std::vector<Rate>& floors,
                         bool inArrears, Real redemption,
                         const Date& issueDate,
                         const Period& exCouponPeriod,
                         const py::object& exCouponCalendar,
                         BusinessDayConvention exCouponConvention,
                         bool exCouponEndOfMonth) {
            Natural fd = Null<Natural>();
            if (!fixingDays.is_none())
                fd = fixingDays.cast<Natural>();
            Calendar exCal;
            if (!exCouponCalendar.is_none())
                exCal = exCouponCalendar.cast<Calendar>();
            return ext::make_shared<FloatingRateBond>(
                settlementDays, faceAmount, std::move(schedule), iborIndex,
                accrualDayCounter, paymentConvention, fd,
                gearings, spreads, caps, floors,
                inArrears, redemption, issueDate,
                exCouponPeriod, exCal,
                exCouponConvention, exCouponEndOfMonth);
        }),
            py::arg("settlementDays"),
            py::arg("faceAmount"),
            py::arg("schedule"),
            py::arg("iborIndex"),
            py::arg("accrualDayCounter"),
            py::arg("paymentConvention") = Following,
            py::arg("fixingDays") = py::none(),
            py::arg("gearings") = std::vector<Real>{1.0},
            py::arg("spreads") = std::vector<Spread>{0.0},
            py::arg("caps") = std::vector<Rate>{},
            py::arg("floors") = std::vector<Rate>{},
            py::arg("inArrears") = false,
            py::arg("redemption") = 100.0,
            py::arg("issueDate") = Date(),
            py::arg("exCouponPeriod") = Period(),
            py::arg("exCouponCalendar") = py::none(),
            py::arg("exCouponConvention") = Unadjusted,
            py::arg("exCouponEndOfMonth") = false,
            "Constructs a floating rate bond.");
}
