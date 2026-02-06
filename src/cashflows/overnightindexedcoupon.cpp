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
#include <ql/cashflows/overnightindexedcoupon.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::overnightindexedcoupon(py::module_& m) {
    // RateAveraging enum (used by OvernightIndexedCoupon and SwaptionHelper)
    py::class_<RateAveraging> rateAvg(m, "RateAveraging",
        "Rate averaging methods for multi-fixing coupons.");
    py::enum_<RateAveraging::Type>(rateAvg, "Type",
        "Rate averaging type.")
        .value("Simple", RateAveraging::Simple,
            "Simple averaging: sum of sub-period interest amounts.")
        .value("Compound", RateAveraging::Compound,
            "Compound averaging: compounded sub-period rates.");

    py::class_<OvernightIndexedCoupon, FloatingRateCoupon,
               ext::shared_ptr<OvernightIndexedCoupon>>(
        m, "OvernightIndexedCoupon",
        "Coupon paying the compounded daily overnight rate.")
        .def(py::init([](const Date& paymentDate, Real nominal,
                         const Date& startDate, const Date& endDate,
                         const ext::shared_ptr<OvernightIndex>& index,
                         Real gearing, Spread spread,
                         const Date& refPeriodStart, const Date& refPeriodEnd,
                         const py::object& dayCounter,
                         bool telescopicValueDates,
                         RateAveraging::Type averagingMethod,
                         const py::object& lookbackDays,
                         Natural lockoutDays,
                         bool applyObservationShift) {
            DayCounter dc;
            if (!dayCounter.is_none())
                dc = dayCounter.cast<DayCounter>();
            Natural lb = Null<Natural>();
            if (!lookbackDays.is_none())
                lb = lookbackDays.cast<Natural>();
            return ext::make_shared<OvernightIndexedCoupon>(
                paymentDate, nominal, startDate, endDate, index,
                gearing, spread, refPeriodStart, refPeriodEnd, dc,
                telescopicValueDates, averagingMethod,
                lb, lockoutDays, applyObservationShift);
        }),
             py::arg("paymentDate"), py::arg("nominal"),
             py::arg("startDate"), py::arg("endDate"),
             py::arg("overnightIndex"),
             py::arg("gearing") = 1.0, py::arg("spread") = 0.0,
             py::arg("refPeriodStart") = Date(), py::arg("refPeriodEnd") = Date(),
             py::arg("dayCounter") = py::none(),
             py::arg("telescopicValueDates") = false,
             py::arg("averagingMethod") = RateAveraging::Compound,
             py::arg("lookbackDays") = py::none(),
             py::arg("lockoutDays") = 0,
             py::arg("applyObservationShift") = false,
             "Constructs an overnight indexed coupon.")
        .def("fixingDates", &OvernightIndexedCoupon::fixingDates,
             py::return_value_policy::reference_internal,
             "Returns the fixing dates for the rates to be compounded.")
        .def("dt", &OvernightIndexedCoupon::dt,
             py::return_value_policy::reference_internal,
             "Returns the accrual periods.")
        .def("indexFixings", &OvernightIndexedCoupon::indexFixings,
             "Returns the fixings to be compounded.")
        .def("valueDates", &OvernightIndexedCoupon::valueDates,
             py::return_value_policy::reference_internal,
             "Returns the value dates for the rates to be compounded.")
        .def("averagingMethod", &OvernightIndexedCoupon::averagingMethod,
             "Returns the averaging method.")
        .def("lockoutDays", &OvernightIndexedCoupon::lockoutDays,
             "Returns the number of lockout days.")
        .def("applyObservationShift", &OvernightIndexedCoupon::applyObservationShift,
             "Returns whether observation shift is applied.");

    // OvernightLeg builder
    py::class_<OvernightLeg>(m, "OvernightLeg",
        "Helper class for building a leg of overnight indexed coupons.")
        .def(py::init<Schedule, ext::shared_ptr<OvernightIndex>>(),
             py::arg("schedule"), py::arg("overnightIndex"),
             "Constructs an OvernightLeg from a schedule and overnight index.")
        .def("withNotionals",
            [](OvernightLeg& self, Real n) -> OvernightLeg& {
                return self.withNotionals(n);
            },
            py::return_value_policy::reference_internal, py::arg("nominal"))
        .def("withNotionals",
            [](OvernightLeg& self, const std::vector<Real>& n) -> OvernightLeg& {
                return self.withNotionals(n);
            },
            py::return_value_policy::reference_internal, py::arg("nominals"))
        .def("withPaymentDayCounter",
            [](OvernightLeg& self, const DayCounter& dc) -> OvernightLeg& {
                return self.withPaymentDayCounter(dc);
            },
            py::return_value_policy::reference_internal, py::arg("dayCounter"))
        .def("withPaymentAdjustment",
            [](OvernightLeg& self, BusinessDayConvention bdc) -> OvernightLeg& {
                return self.withPaymentAdjustment(bdc);
            },
            py::return_value_policy::reference_internal, py::arg("convention"))
        .def("withPaymentCalendar",
            [](OvernightLeg& self, const Calendar& cal) -> OvernightLeg& {
                return self.withPaymentCalendar(cal);
            },
            py::return_value_policy::reference_internal, py::arg("calendar"))
        .def("withPaymentLag",
            [](OvernightLeg& self, Integer lag) -> OvernightLeg& {
                return self.withPaymentLag(lag);
            },
            py::return_value_policy::reference_internal, py::arg("lag"))
        .def("withGearings",
            [](OvernightLeg& self, Real g) -> OvernightLeg& {
                return self.withGearings(g);
            },
            py::return_value_policy::reference_internal, py::arg("gearing"))
        .def("withGearings",
            [](OvernightLeg& self, const std::vector<Real>& g) -> OvernightLeg& {
                return self.withGearings(g);
            },
            py::return_value_policy::reference_internal, py::arg("gearings"))
        .def("withSpreads",
            [](OvernightLeg& self, Spread s) -> OvernightLeg& {
                return self.withSpreads(s);
            },
            py::return_value_policy::reference_internal, py::arg("spread"))
        .def("withSpreads",
            [](OvernightLeg& self, const std::vector<Spread>& s) -> OvernightLeg& {
                return self.withSpreads(s);
            },
            py::return_value_policy::reference_internal, py::arg("spreads"))
        .def("withTelescopicValueDates",
            [](OvernightLeg& self, bool flag) -> OvernightLeg& {
                return self.withTelescopicValueDates(flag);
            },
            py::return_value_policy::reference_internal, py::arg("telescopicValueDates"))
        .def("withAveragingMethod",
            [](OvernightLeg& self, RateAveraging::Type method) -> OvernightLeg& {
                return self.withAveragingMethod(method);
            },
            py::return_value_policy::reference_internal, py::arg("averagingMethod"))
        .def("withLookbackDays",
            [](OvernightLeg& self, Natural days) -> OvernightLeg& {
                return self.withLookbackDays(days);
            },
            py::return_value_policy::reference_internal, py::arg("lookbackDays"))
        .def("withLockoutDays",
            [](OvernightLeg& self, Natural days) -> OvernightLeg& {
                return self.withLockoutDays(days);
            },
            py::return_value_policy::reference_internal, py::arg("lockoutDays"))
        .def("withObservationShift",
            [](OvernightLeg& self, bool flag) -> OvernightLeg& {
                return self.withObservationShift(flag);
            },
            py::return_value_policy::reference_internal,
            py::arg("applyObservationShift") = true)
        .def("build",
             [](const OvernightLeg& self) {
                 return static_cast<Leg>(self);
             },
             "Builds and returns the leg of cash flows.");
}
