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
#include <ql/instruments/bonds/convertiblebonds.hpp>
#include <ql/exercise.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/time/daycounter.hpp>
#include <ql/time/schedule.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::convertiblebonds(py::module_& m) {
    // SoftCallability (subclass of Callability)
    py::class_<SoftCallability, Callability, ext::shared_ptr<SoftCallability>>(
        m, "SoftCallability",
        "Callability with a trigger level for soft-call provisions.")
        .def(py::init<const Bond::Price&, const Date&, Real>(),
            py::arg("price"),
            py::arg("date"),
            py::arg("trigger"),
            "Constructs a soft callability with price, date, and trigger.")
        .def("trigger", &SoftCallability::trigger,
            "Returns the trigger level.");

    // ConvertibleBond (base class, protected ctor -- not constructible)
    py::class_<ConvertibleBond, Bond, ext::shared_ptr<ConvertibleBond>>(
        m, "ConvertibleBond",
        "Base class for convertible bonds.")
        .def("conversionRatio", &ConvertibleBond::conversionRatio,
            "Returns the conversion ratio.")
        .def("callability", &ConvertibleBond::callability,
            py::return_value_policy::reference_internal,
            "Returns the callability schedule.");

    // ConvertibleZeroCouponBond
    py::class_<ConvertibleZeroCouponBond, ConvertibleBond,
               ext::shared_ptr<ConvertibleZeroCouponBond>>(
        m, "ConvertibleZeroCouponBond",
        "Convertible zero-coupon bond.")
        .def(py::init<const ext::shared_ptr<Exercise>&,
                       Real,
                       const CallabilitySchedule&,
                       const Date&,
                       Natural,
                       const DayCounter&,
                       const Schedule&,
                       Real>(),
            py::arg("exercise"),
            py::arg("conversionRatio"),
            py::arg("callability"),
            py::arg("issueDate"),
            py::arg("settlementDays"),
            py::arg("dayCounter"),
            py::arg("schedule"),
            py::arg("redemption") = 100.0,
            "Constructs a convertible zero-coupon bond.");

    // ConvertibleFixedCouponBond
    py::class_<ConvertibleFixedCouponBond, ConvertibleBond,
               ext::shared_ptr<ConvertibleFixedCouponBond>>(
        m, "ConvertibleFixedCouponBond",
        "Convertible fixed-coupon bond.")
        .def(py::init([](const ext::shared_ptr<Exercise>& exercise,
                         Real conversionRatio,
                         const CallabilitySchedule& callability,
                         const Date& issueDate,
                         Natural settlementDays,
                         const std::vector<Rate>& coupons,
                         const DayCounter& dayCounter,
                         const Schedule& schedule,
                         Real redemption,
                         const Period& exCouponPeriod,
                         const py::object& exCouponCalendar,
                         BusinessDayConvention exCouponConvention,
                         bool exCouponEndOfMonth) {
            Calendar exCal;
            if (!exCouponCalendar.is_none())
                exCal = exCouponCalendar.cast<Calendar>();
            return ext::make_shared<ConvertibleFixedCouponBond>(
                exercise, conversionRatio, callability, issueDate,
                settlementDays, coupons, dayCounter, schedule, redemption,
                exCouponPeriod, exCal, exCouponConvention, exCouponEndOfMonth);
        }),
            py::arg("exercise"),
            py::arg("conversionRatio"),
            py::arg("callability"),
            py::arg("issueDate"),
            py::arg("settlementDays"),
            py::arg("coupons"),
            py::arg("dayCounter"),
            py::arg("schedule"),
            py::arg("redemption") = 100.0,
            py::arg("exCouponPeriod") = Period(),
            py::arg("exCouponCalendar") = py::none(),
            py::arg("exCouponConvention") = Unadjusted,
            py::arg("exCouponEndOfMonth") = false,
            "Constructs a convertible fixed-coupon bond.");

    // ConvertibleFloatingRateBond
    py::class_<ConvertibleFloatingRateBond, ConvertibleBond,
               ext::shared_ptr<ConvertibleFloatingRateBond>>(
        m, "ConvertibleFloatingRateBond",
        "Convertible floating-rate bond.")
        .def(py::init([](const ext::shared_ptr<Exercise>& exercise,
                         Real conversionRatio,
                         const CallabilitySchedule& callability,
                         const Date& issueDate,
                         Natural settlementDays,
                         const ext::shared_ptr<IborIndex>& index,
                         Natural fixingDays,
                         const std::vector<Spread>& spreads,
                         const DayCounter& dayCounter,
                         const Schedule& schedule,
                         Real redemption,
                         const Period& exCouponPeriod,
                         const py::object& exCouponCalendar,
                         BusinessDayConvention exCouponConvention,
                         bool exCouponEndOfMonth) {
            Calendar exCal;
            if (!exCouponCalendar.is_none())
                exCal = exCouponCalendar.cast<Calendar>();
            return ext::make_shared<ConvertibleFloatingRateBond>(
                exercise, conversionRatio, callability, issueDate,
                settlementDays, index, fixingDays, spreads,
                dayCounter, schedule, redemption,
                exCouponPeriod, exCal, exCouponConvention, exCouponEndOfMonth);
        }),
            py::arg("exercise"),
            py::arg("conversionRatio"),
            py::arg("callability"),
            py::arg("issueDate"),
            py::arg("settlementDays"),
            py::arg("index"),
            py::arg("fixingDays"),
            py::arg("spreads"),
            py::arg("dayCounter"),
            py::arg("schedule"),
            py::arg("redemption") = 100.0,
            py::arg("exCouponPeriod") = Period(),
            py::arg("exCouponCalendar") = py::none(),
            py::arg("exCouponConvention") = Unadjusted,
            py::arg("exCouponEndOfMonth") = false,
            "Constructs a convertible floating-rate bond.");
}
