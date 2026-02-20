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
#include <ql/instruments/bonds/cpibond.hpp>
#include <ql/indexes/inflationindex.hpp>
#include <ql/time/schedule.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::cpibond(py::module_& m) {
    py::class_<CPIBond, Bond, ext::shared_ptr<CPIBond>>(
        m, "CPIBond",
        "CPI inflation-linked bond.")
        .def(py::init([](Natural settlementDays,
                         Real faceAmount,
                         Real baseCPI,
                         const Period& observationLag,
                         const ext::shared_ptr<ZeroInflationIndex>& cpiIndex,
                         CPI::InterpolationType observationInterpolation,
                         Schedule schedule,
                         const std::vector<Rate>& coupons,
                         const DayCounter& accrualDayCounter,
                         BusinessDayConvention paymentConvention,
                         const Date& issueDate,
                         const py::object& paymentCalendar,
                         const Period& exCouponPeriod,
                         const py::object& exCouponCalendar,
                         BusinessDayConvention exCouponConvention,
                         bool exCouponEndOfMonth) {
            Calendar payCal;
            if (!paymentCalendar.is_none())
                payCal = paymentCalendar.cast<Calendar>();
            Calendar exCal;
            if (!exCouponCalendar.is_none())
                exCal = exCouponCalendar.cast<Calendar>();
            return ext::make_shared<CPIBond>(
                settlementDays, faceAmount, baseCPI, observationLag,
                cpiIndex, observationInterpolation, std::move(schedule),
                coupons, accrualDayCounter, paymentConvention, issueDate,
                payCal, exCouponPeriod, exCal,
                exCouponConvention, exCouponEndOfMonth);
        }),
            py::arg("settlementDays"),
            py::arg("faceAmount"),
            py::arg("baseCPI"),
            py::arg("observationLag"),
            py::arg("cpiIndex"),
            py::arg("observationInterpolation"),
            py::arg("schedule"),
            py::arg("coupons"),
            py::arg("accrualDayCounter"),
            py::arg("paymentConvention") = ModifiedFollowing,
            py::arg("issueDate") = Date(),
            py::arg("paymentCalendar") = py::none(),
            py::arg("exCouponPeriod") = Period(),
            py::arg("exCouponCalendar") = py::none(),
            py::arg("exCouponConvention") = Unadjusted,
            py::arg("exCouponEndOfMonth") = false,
            "Constructs a CPI inflation-linked bond.")
        .def("frequency", &CPIBond::frequency,
            "Returns the coupon frequency.")
        .def("dayCounter", &CPIBond::dayCounter,
            py::return_value_policy::reference_internal,
            "Returns the accrual day counter.")
        .def("growthOnly", &CPIBond::growthOnly,
            "Returns true if the bond pays growth only.")
        .def("baseCPI", &CPIBond::baseCPI,
            "Returns the base CPI value.")
        .def("observationLag", &CPIBond::observationLag,
            "Returns the observation lag.")
        .def("cpiIndex", &CPIBond::cpiIndex,
            "Returns the CPI index.")
        .def("observationInterpolation", &CPIBond::observationInterpolation,
            "Returns the observation interpolation type.");
}
