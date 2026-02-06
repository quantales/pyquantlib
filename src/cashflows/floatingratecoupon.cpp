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
#include <ql/cashflows/floatingratecoupon.hpp>
#include <ql/cashflows/couponpricer.hpp>
#include <ql/indexes/interestrateindex.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::floatingratecoupon(py::module_& m) {
    py::class_<FloatingRateCoupon, Coupon, ext::shared_ptr<FloatingRateCoupon>>(
        m, "FloatingRateCoupon",
        "Coupon paying a variable index-based rate.")
        .def(py::init([](const Date& paymentDate, Real nominal,
                         const Date& startDate, const Date& endDate,
                         Natural fixingDays,
                         const ext::shared_ptr<InterestRateIndex>& index,
                         Real gearing, Spread spread,
                         const Date& refPeriodStart, const Date& refPeriodEnd,
                         const py::object& dayCounter,
                         bool isInArrears, const Date& exCouponDate) {
            DayCounter dc;
            if (!dayCounter.is_none())
                dc = dayCounter.cast<DayCounter>();
            return ext::make_shared<FloatingRateCoupon>(
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
             "Constructs a floating-rate coupon.")
        .def("index", &FloatingRateCoupon::index,
             "Returns the floating index.")
        .def("fixingDays", &FloatingRateCoupon::fixingDays,
             "Returns the number of fixing days.")
        .def("fixingDate", &FloatingRateCoupon::fixingDate,
             "Returns the fixing date.")
        .def("gearing", &FloatingRateCoupon::gearing,
             "Returns the index gearing.")
        .def("spread", &FloatingRateCoupon::spread,
             "Returns the spread over the index fixing.")
        .def("indexFixing", &FloatingRateCoupon::indexFixing,
             "Returns the fixing of the underlying index.")
        .def("convexityAdjustment", &FloatingRateCoupon::convexityAdjustment,
             "Returns the convexity adjustment.")
        .def("adjustedFixing", &FloatingRateCoupon::adjustedFixing,
             "Returns the convexity-adjusted fixing.")
        .def("isInArrears", &FloatingRateCoupon::isInArrears,
             "Returns whether the coupon fixes in arrears.")
        .def("setPricer", &FloatingRateCoupon::setPricer,
             py::arg("pricer"),
             "Sets the coupon pricer.")
        .def("pricer", &FloatingRateCoupon::pricer,
             "Returns the coupon pricer.");
}
