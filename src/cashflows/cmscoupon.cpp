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
#include <ql/cashflows/cmscoupon.hpp>
#include <ql/indexes/swapindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::cmscoupon(py::module_& m) {
    py::class_<CmsCoupon, FloatingRateCoupon, ext::shared_ptr<CmsCoupon>>(
        m, "CmsCoupon",
        "Coupon paying a CMS swap rate.")
        .def(py::init([](const Date& paymentDate, Real nominal,
                         const Date& startDate, const Date& endDate,
                         Natural fixingDays,
                         const ext::shared_ptr<SwapIndex>& index,
                         Real gearing, Spread spread,
                         const Date& refPeriodStart, const Date& refPeriodEnd,
                         const py::object& dayCounter,
                         bool isInArrears, const Date& exCouponDate) {
            DayCounter dc;
            if (!dayCounter.is_none())
                dc = dayCounter.cast<DayCounter>();
            return ext::make_shared<CmsCoupon>(
                paymentDate, nominal, startDate, endDate, fixingDays,
                index, gearing, spread, refPeriodStart, refPeriodEnd,
                dc, isInArrears, exCouponDate);
        }),
            py::arg("paymentDate"), py::arg("nominal"),
            py::arg("startDate"), py::arg("endDate"),
            py::arg("fixingDays"), py::arg("index"),
            py::arg("gearing") = 1.0, py::arg("spread") = 0.0,
            py::arg("refPeriodStart") = Date(), py::arg("refPeriodEnd") = Date(),
            py::arg("dayCounter") = py::none(),
            py::arg("isInArrears") = false, py::arg("exCouponDate") = Date(),
            "Constructs a CMS coupon.")
        .def("swapIndex", &CmsCoupon::swapIndex,
            "Returns the underlying swap index.");

    // CmsLeg builder
    py::class_<CmsLeg>(m, "CmsLeg",
        "Helper class for building a leg of CMS coupons.")
        .def(py::init<Schedule, ext::shared_ptr<SwapIndex>>(),
            py::arg("schedule"), py::arg("swapIndex"),
            "Constructs a CmsLeg from a schedule and swap index.")
        .def("withNotionals",
            [](CmsLeg& self, Real n) -> CmsLeg& {
                return self.withNotionals(n);
            },
            py::return_value_policy::reference_internal, py::arg("nominal"))
        .def("withNotionals",
            [](CmsLeg& self, const std::vector<Real>& n) -> CmsLeg& {
                return self.withNotionals(n);
            },
            py::return_value_policy::reference_internal, py::arg("nominals"))
        .def("withPaymentDayCounter",
            [](CmsLeg& self, const DayCounter& dc) -> CmsLeg& {
                return self.withPaymentDayCounter(dc);
            },
            py::return_value_policy::reference_internal, py::arg("dayCounter"))
        .def("withPaymentAdjustment",
            [](CmsLeg& self, BusinessDayConvention bdc) -> CmsLeg& {
                return self.withPaymentAdjustment(bdc);
            },
            py::return_value_policy::reference_internal, py::arg("convention"))
        .def("withFixingDays",
            [](CmsLeg& self, Natural days) -> CmsLeg& {
                return self.withFixingDays(days);
            },
            py::return_value_policy::reference_internal, py::arg("fixingDays"))
        .def("withFixingDays",
            [](CmsLeg& self, const std::vector<Natural>& days) -> CmsLeg& {
                return self.withFixingDays(days);
            },
            py::return_value_policy::reference_internal, py::arg("fixingDays"))
        .def("withGearings",
            [](CmsLeg& self, Real g) -> CmsLeg& {
                return self.withGearings(g);
            },
            py::return_value_policy::reference_internal, py::arg("gearing"))
        .def("withGearings",
            [](CmsLeg& self, const std::vector<Real>& g) -> CmsLeg& {
                return self.withGearings(g);
            },
            py::return_value_policy::reference_internal, py::arg("gearings"))
        .def("withSpreads",
            [](CmsLeg& self, Spread s) -> CmsLeg& {
                return self.withSpreads(s);
            },
            py::return_value_policy::reference_internal, py::arg("spread"))
        .def("withSpreads",
            [](CmsLeg& self, const std::vector<Spread>& s) -> CmsLeg& {
                return self.withSpreads(s);
            },
            py::return_value_policy::reference_internal, py::arg("spreads"))
        .def("withCaps",
            [](CmsLeg& self, Rate cap) -> CmsLeg& {
                return self.withCaps(cap);
            },
            py::return_value_policy::reference_internal, py::arg("cap"))
        .def("withCaps",
            [](CmsLeg& self, const std::vector<Rate>& caps) -> CmsLeg& {
                return self.withCaps(caps);
            },
            py::return_value_policy::reference_internal, py::arg("caps"))
        .def("withFloors",
            [](CmsLeg& self, Rate floor) -> CmsLeg& {
                return self.withFloors(floor);
            },
            py::return_value_policy::reference_internal, py::arg("floor"))
        .def("withFloors",
            [](CmsLeg& self, const std::vector<Rate>& floors) -> CmsLeg& {
                return self.withFloors(floors);
            },
            py::return_value_policy::reference_internal, py::arg("floors"))
        .def("inArrears",
            [](CmsLeg& self, bool flag) -> CmsLeg& {
                return self.inArrears(flag);
            },
            py::return_value_policy::reference_internal, py::arg("flag") = true)
        .def("withZeroPayments",
            [](CmsLeg& self, bool flag) -> CmsLeg& {
                return self.withZeroPayments(flag);
            },
            py::return_value_policy::reference_internal, py::arg("flag") = true)
        .def("withExCouponPeriod",
            [](CmsLeg& self, const Period& p, const Calendar& cal,
               BusinessDayConvention bdc, bool eom) -> CmsLeg& {
                return self.withExCouponPeriod(p, cal, bdc, eom);
            },
            py::return_value_policy::reference_internal,
            py::arg("period"), py::arg("calendar"),
            py::arg("convention"), py::arg("endOfMonth") = false)
        .def("build",
            [](const CmsLeg& self) {
                return static_cast<Leg>(self);
            },
            "Builds and returns the leg of cash flows.");
}
