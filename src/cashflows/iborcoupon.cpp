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
#include <ql/cashflows/iborcoupon.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::iborcoupon(py::module_& m) {
    py::class_<IborCoupon, FloatingRateCoupon, ext::shared_ptr<IborCoupon>>(
        m, "IborCoupon",
        "Coupon paying a Libor-type index.")
        .def(py::init([](const Date& paymentDate, Real nominal,
                         const Date& startDate, const Date& endDate,
                         Natural fixingDays,
                         const ext::shared_ptr<IborIndex>& index,
                         Real gearing, Spread spread,
                         const Date& refPeriodStart, const Date& refPeriodEnd,
                         const py::object& dayCounter,
                         bool isInArrears, const Date& exCouponDate) {
            DayCounter dc;
            if (!dayCounter.is_none())
                dc = dayCounter.cast<DayCounter>();
            return ext::make_shared<IborCoupon>(
                paymentDate, nominal, startDate, endDate, fixingDays, index,
                gearing, spread, refPeriodStart, refPeriodEnd, dc,
                isInArrears, exCouponDate);
        }),
             py::arg("paymentDate"), py::arg("nominal"),
             py::arg("startDate"), py::arg("endDate"),
             py::arg("fixingDays"), py::arg("index"),
             py::arg("gearing") = 1.0, py::arg("spread") = 0.0,
             py::arg("refPeriodStart") = Date(), py::arg("refPeriodEnd") = Date(),
             py::arg("dayCounter") = py::none(),
             py::arg("isInArrears") = false, py::arg("exCouponDate") = Date(),
             "Constructs an Ibor coupon.")
        .def("iborIndex", &IborCoupon::iborIndex,
             "Returns the Ibor index.")
        .def("fixingDate", &IborCoupon::fixingDate,
             "Returns the fixing date.")
        .def("fixingValueDate", &IborCoupon::fixingValueDate,
             "Returns the start of the deposit period underlying the fixing.")
        .def("fixingMaturityDate", &IborCoupon::fixingMaturityDate,
             "Returns the end of the deposit period underlying the fixing.")
        .def("fixingEndDate", &IborCoupon::fixingEndDate,
             "Returns the end of the deposit period underlying the coupon fixing.")
        .def("spanningTime", &IborCoupon::spanningTime,
             "Returns the period underlying the coupon fixing as a year fraction.");

    // IborCoupon::Settings singleton
    py::class_<IborCoupon::Settings>(m, "IborCouponSettings",
        "Per-session settings for IborCoupon class.")
        .def_static("instance", &IborCoupon::Settings::instance,
             py::return_value_policy::reference,
             "Returns the singleton instance.")
        .def("createAtParCoupons", &IborCoupon::Settings::createAtParCoupons,
             "Switches to par coupon creation.")
        .def("createIndexedCoupons", &IborCoupon::Settings::createIndexedCoupons,
             "Switches to indexed coupon creation.")
        .def("usingAtParCoupons", &IborCoupon::Settings::usingAtParCoupons,
             "Returns whether par coupons are being used.");

    // IborLeg builder
    py::class_<IborLeg>(m, "IborLeg",
        "Helper class for building a leg of Ibor coupons.")
        .def(py::init<Schedule, ext::shared_ptr<IborIndex>>(),
             py::arg("schedule"), py::arg("index"),
             "Constructs an IborLeg from a schedule and index.")
        .def("withNotionals",
            [](IborLeg& self, Real n) -> IborLeg& {
                return self.withNotionals(n);
            },
            py::return_value_policy::reference_internal, py::arg("nominal"))
        .def("withNotionals",
            [](IborLeg& self, const std::vector<Real>& n) -> IborLeg& {
                return self.withNotionals(n);
            },
            py::return_value_policy::reference_internal, py::arg("nominals"))
        .def("withPaymentDayCounter",
            [](IborLeg& self, const DayCounter& dc) -> IborLeg& {
                return self.withPaymentDayCounter(dc);
            },
            py::return_value_policy::reference_internal, py::arg("dayCounter"))
        .def("withPaymentAdjustment",
            [](IborLeg& self, BusinessDayConvention bdc) -> IborLeg& {
                return self.withPaymentAdjustment(bdc);
            },
            py::return_value_policy::reference_internal, py::arg("convention"))
        .def("withPaymentLag",
            [](IborLeg& self, Integer lag) -> IborLeg& {
                return self.withPaymentLag(lag);
            },
            py::return_value_policy::reference_internal, py::arg("lag"))
        .def("withPaymentCalendar",
            [](IborLeg& self, const Calendar& cal) -> IborLeg& {
                return self.withPaymentCalendar(cal);
            },
            py::return_value_policy::reference_internal, py::arg("calendar"))
        .def("withFixingDays",
            [](IborLeg& self, Natural days) -> IborLeg& {
                return self.withFixingDays(days);
            },
            py::return_value_policy::reference_internal, py::arg("fixingDays"))
        .def("withFixingDays",
            [](IborLeg& self, const std::vector<Natural>& days) -> IborLeg& {
                return self.withFixingDays(days);
            },
            py::return_value_policy::reference_internal, py::arg("fixingDays"))
        .def("withGearings",
            [](IborLeg& self, Real g) -> IborLeg& {
                return self.withGearings(g);
            },
            py::return_value_policy::reference_internal, py::arg("gearing"))
        .def("withGearings",
            [](IborLeg& self, const std::vector<Real>& g) -> IborLeg& {
                return self.withGearings(g);
            },
            py::return_value_policy::reference_internal, py::arg("gearings"))
        .def("withSpreads",
            [](IborLeg& self, Spread s) -> IborLeg& {
                return self.withSpreads(s);
            },
            py::return_value_policy::reference_internal, py::arg("spread"))
        .def("withSpreads",
            [](IborLeg& self, const std::vector<Spread>& s) -> IborLeg& {
                return self.withSpreads(s);
            },
            py::return_value_policy::reference_internal, py::arg("spreads"))
        .def("withCaps",
            [](IborLeg& self, Rate cap) -> IborLeg& {
                return self.withCaps(cap);
            },
            py::return_value_policy::reference_internal, py::arg("cap"))
        .def("withCaps",
            [](IborLeg& self, const std::vector<Rate>& caps) -> IborLeg& {
                return self.withCaps(caps);
            },
            py::return_value_policy::reference_internal, py::arg("caps"))
        .def("withFloors",
            [](IborLeg& self, Rate floor) -> IborLeg& {
                return self.withFloors(floor);
            },
            py::return_value_policy::reference_internal, py::arg("floor"))
        .def("withFloors",
            [](IborLeg& self, const std::vector<Rate>& floors) -> IborLeg& {
                return self.withFloors(floors);
            },
            py::return_value_policy::reference_internal, py::arg("floors"))
        .def("inArrears",
            [](IborLeg& self, bool flag) -> IborLeg& {
                return self.inArrears(flag);
            },
            py::return_value_policy::reference_internal, py::arg("flag") = true)
        .def("withZeroPayments",
            [](IborLeg& self, bool flag) -> IborLeg& {
                return self.withZeroPayments(flag);
            },
            py::return_value_policy::reference_internal, py::arg("flag") = true)
        .def("withExCouponPeriod",
            [](IborLeg& self, const Period& p, const Calendar& cal,
               BusinessDayConvention bdc, bool eom) -> IborLeg& {
                return self.withExCouponPeriod(p, cal, bdc, eom);
            },
            py::return_value_policy::reference_internal,
            py::arg("period"), py::arg("calendar"),
            py::arg("convention"), py::arg("endOfMonth") = false)
        .def("build",
             [](const IborLeg& self) {
                 return static_cast<Leg>(self);
             },
             "Builds and returns the leg of cash flows.");
}
