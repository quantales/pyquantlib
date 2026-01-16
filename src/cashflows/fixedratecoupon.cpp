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
#include <ql/cashflows/fixedratecoupon.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::fixedratecoupon(py::module_& m) {
    py::class_<FixedRateCoupon, Coupon, ext::shared_ptr<FixedRateCoupon>>(m, "FixedRateCoupon",
        "Coupon paying a fixed interest rate.")
        .def(py::init<const Date&, Real, const InterestRate&,
                      const Date&, const Date&,
                      const Date&, const Date&, const Date&>(),
             py::arg("paymentDate"), py::arg("nominal"), py::arg("interestRate"),
             py::arg("accrualStartDate"), py::arg("accrualEndDate"),
             py::arg("refPeriodStart") = Date(), py::arg("refPeriodEnd") = Date(),
             py::arg("exCouponDate") = Date(),
             "Constructs a fixed-rate coupon from an InterestRate.")
        .def(py::init<const Date&, Real, Rate, const DayCounter&,
                      const Date&, const Date&,
                      const Date&, const Date&, const Date&>(),
             py::arg("paymentDate"), py::arg("nominal"), py::arg("rate"), py::arg("dayCounter"),
             py::arg("accrualStartDate"), py::arg("accrualEndDate"),
             py::arg("refPeriodStart") = Date(), py::arg("refPeriodEnd") = Date(),
             py::arg("exCouponDate") = Date(),
             "Constructs a fixed-rate coupon from rate and day counter.")
        .def("interestRate", &FixedRateCoupon::interestRate,
             py::return_value_policy::reference_internal,
             "Returns the interest rate.");

    py::class_<FixedRateLeg>(m, "FixedRateLeg",
        "Helper class for building a leg of fixed-rate coupons.")
        .def(py::init<const Schedule&>(),
             py::arg("schedule"),
             "Constructs a FixedRateLeg from a schedule.")
        .def("withNotionals",
            [](FixedRateLeg& self, Real n) -> FixedRateLeg& {
                return self.withNotionals(n);
            },
            py::return_value_policy::reference_internal, py::arg("nominal"))
        .def("withNotionals",
            [](FixedRateLeg& self, const std::vector<Real>& n) -> FixedRateLeg& {
                return self.withNotionals(n);
            },
            py::return_value_policy::reference_internal, py::arg("nominals"))
        .def("withCouponRates",
            [](FixedRateLeg& self, Rate r, const DayCounter& dc,
               Compounding comp, Frequency freq) -> FixedRateLeg& {
                return self.withCouponRates(r, dc, comp, freq);
            },
            py::return_value_policy::reference_internal,
            py::arg("rate"), py::arg("dayCounter"),
            py::arg("compounding") = Simple, py::arg("frequency") = Annual)
        .def("withCouponRates",
            [](FixedRateLeg& self, const InterestRate& ir) -> FixedRateLeg& {
                return self.withCouponRates(ir);
            },
            py::return_value_policy::reference_internal, py::arg("interestRate"))
        .def("withCouponRates",
            [](FixedRateLeg& self, const std::vector<Rate>& r, const DayCounter& dc,
               Compounding comp, Frequency freq) -> FixedRateLeg& {
                return self.withCouponRates(r, dc, comp, freq);
            },
            py::return_value_policy::reference_internal,
            py::arg("rates"), py::arg("dayCounter"),
            py::arg("compounding") = Simple, py::arg("frequency") = Annual)
        .def("withCouponRates",
            [](FixedRateLeg& self, const std::vector<InterestRate>& ir) -> FixedRateLeg& {
                return self.withCouponRates(ir);
            },
            py::return_value_policy::reference_internal, py::arg("interestRates"))
        .def("withPaymentAdjustment",
            [](FixedRateLeg& self, BusinessDayConvention bdc) -> FixedRateLeg& {
                return self.withPaymentAdjustment(bdc);
            },
            py::return_value_policy::reference_internal, py::arg("convention"))
        .def("withFirstPeriodDayCounter",
            [](FixedRateLeg& self, const DayCounter& dc) -> FixedRateLeg& {
                return self.withFirstPeriodDayCounter(dc);
            },
            py::return_value_policy::reference_internal, py::arg("dayCounter"))
        .def("withLastPeriodDayCounter",
            [](FixedRateLeg& self, const DayCounter& dc) -> FixedRateLeg& {
                return self.withLastPeriodDayCounter(dc);
            },
            py::return_value_policy::reference_internal, py::arg("dayCounter"))
        .def("withPaymentCalendar",
            [](FixedRateLeg& self, const Calendar& cal) -> FixedRateLeg& {
                return self.withPaymentCalendar(cal);
            },
            py::return_value_policy::reference_internal, py::arg("calendar"))
        .def("withPaymentLag",
            [](FixedRateLeg& self, Integer lag) -> FixedRateLeg& {
                return self.withPaymentLag(lag);
            },
            py::return_value_policy::reference_internal, py::arg("lag"))
        .def("withExCouponPeriod",
            [](FixedRateLeg& self, const Period& period, const Calendar& cal,
               BusinessDayConvention bdc, bool endOfMonth) -> FixedRateLeg& {
                return self.withExCouponPeriod(period, cal, bdc, endOfMonth);
            },
            py::return_value_policy::reference_internal,
            py::arg("period"), py::arg("calendar"),
            py::arg("convention"), py::arg("endOfMonth") = false)
        .def("build",
             [](const FixedRateLeg& self) {
                 return static_cast<Leg>(self);
             },
             "Builds and returns the leg of cash flows.");
}
