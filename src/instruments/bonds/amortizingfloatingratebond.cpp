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
#include <ql/instruments/bonds/amortizingfloatingratebond.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/time/daycounter.hpp>
#include <ql/time/schedule.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::amortizingfloatingratebond(py::module_& m) {
    py::class_<AmortizingFloatingRateBond, Bond,
               ext::shared_ptr<AmortizingFloatingRateBond>>(
        m, "AmortizingFloatingRateBond",
        "Amortizing floating-rate bond.")
        .def(py::init([](Natural settlementDays,
                         const std::vector<Real>& notionals,
                         Schedule schedule,
                         const ext::shared_ptr<IborIndex>& index,
                         const DayCounter& accrualDayCounter,
                         BusinessDayConvention paymentConvention,
                         const py::object& fixingDays,
                         const std::vector<Real>& gearings,
                         const std::vector<Spread>& spreads,
                         const std::vector<Rate>& caps,
                         const std::vector<Rate>& floors,
                         bool inArrears,
                         const Date& issueDate,
                         const Period& exCouponPeriod,
                         const py::object& exCouponCalendar,
                         BusinessDayConvention exCouponConvention,
                         bool exCouponEndOfMonth,
                         const std::vector<Real>& redemptions,
                         Integer paymentLag) {
            Natural fd = Null<Natural>();
            if (!fixingDays.is_none())
                fd = fixingDays.cast<Natural>();
            Calendar exCal;
            if (!exCouponCalendar.is_none())
                exCal = exCouponCalendar.cast<Calendar>();
            return ext::make_shared<AmortizingFloatingRateBond>(
                settlementDays, notionals, std::move(schedule), index,
                accrualDayCounter, paymentConvention, fd,
                gearings, spreads, caps, floors,
                inArrears, issueDate,
                exCouponPeriod, exCal,
                exCouponConvention, exCouponEndOfMonth,
                redemptions, paymentLag);
        }),
            py::arg("settlementDays"),
            py::arg("notionals"),
            py::arg("schedule"),
            py::arg("index"),
            py::arg("accrualDayCounter"),
            py::arg("paymentConvention") = Following,
            py::arg("fixingDays") = py::none(),
            py::arg("gearings") = std::vector<Real>{1.0},
            py::arg("spreads") = std::vector<Spread>{0.0},
            py::arg("caps") = std::vector<Rate>{},
            py::arg("floors") = std::vector<Rate>{},
            py::arg("inArrears") = false,
            py::arg("issueDate") = Date(),
            py::arg("exCouponPeriod") = Period(),
            py::arg("exCouponCalendar") = py::none(),
            py::arg("exCouponConvention") = Unadjusted,
            py::arg("exCouponEndOfMonth") = false,
            py::arg("redemptions") = std::vector<Real>{100.0},
            py::arg("paymentLag") = 0,
            "Constructs an amortizing floating-rate bond.");
}
