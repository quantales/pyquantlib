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
#include <ql/cashflows/capflooredcoupon.hpp>
#include <ql/cashflows/couponpricer.hpp>
#include <ql/indexes/iborindex.hpp>
#include <ql/indexes/swapindex.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::capflooredcoupon(py::module_& m) {
    // CappedFlooredCoupon
    py::class_<CappedFlooredCoupon, FloatingRateCoupon,
               ext::shared_ptr<CappedFlooredCoupon>>(
        m, "CappedFlooredCoupon",
        "Capped and/or floored floating-rate coupon.")
        .def(py::init([](const ext::shared_ptr<FloatingRateCoupon>& underlying,
                         const py::object& cap, const py::object& floor) {
            Rate c = cap.is_none() ? Null<Rate>() : cap.cast<Rate>();
            Rate f = floor.is_none() ? Null<Rate>() : floor.cast<Rate>();
            return ext::make_shared<CappedFlooredCoupon>(underlying, c, f);
        }),
            py::arg("underlying"),
            py::arg("cap") = py::none(),
            py::arg("floor") = py::none(),
            "Constructs from an underlying coupon with optional cap/floor.")
        .def("rate", &CappedFlooredCoupon::rate,
            "Returns the capped/floored rate.")
        .def("convexityAdjustment", &CappedFlooredCoupon::convexityAdjustment,
            "Returns the convexity adjustment.")
        .def("cap", &CappedFlooredCoupon::cap,
            "Returns the cap rate.")
        .def("floor", &CappedFlooredCoupon::floor,
            "Returns the floor rate.")
        .def("effectiveCap", &CappedFlooredCoupon::effectiveCap,
            "Returns the effective cap of fixing.")
        .def("effectiveFloor", &CappedFlooredCoupon::effectiveFloor,
            "Returns the effective floor of fixing.")
        .def("isCapped", &CappedFlooredCoupon::isCapped,
            "Returns whether the coupon is capped.")
        .def("isFloored", &CappedFlooredCoupon::isFloored,
            "Returns whether the coupon is floored.")
        .def("underlying", &CappedFlooredCoupon::underlying,
            "Returns the underlying floating-rate coupon.")
        .def("setPricer", &CappedFlooredCoupon::setPricer,
            py::arg("pricer"),
            "Sets the coupon pricer.");

    // CappedFlooredIborCoupon
    py::class_<CappedFlooredIborCoupon, CappedFlooredCoupon,
               ext::shared_ptr<CappedFlooredIborCoupon>>(
        m, "CappedFlooredIborCoupon",
        "Capped/floored Ibor coupon.")
        .def(py::init([](const Date& paymentDate, Real nominal,
                         const Date& startDate, const Date& endDate,
                         Natural fixingDays,
                         const ext::shared_ptr<IborIndex>& index,
                         Real gearing, Spread spread,
                         const py::object& cap, const py::object& floor,
                         const Date& refPeriodStart, const Date& refPeriodEnd,
                         const py::object& dayCounter,
                         bool isInArrears, const Date& exCouponDate) {
            Rate c = cap.is_none() ? Null<Rate>() : cap.cast<Rate>();
            Rate f = floor.is_none() ? Null<Rate>() : floor.cast<Rate>();
            DayCounter dc;
            if (!dayCounter.is_none())
                dc = dayCounter.cast<DayCounter>();
            return ext::make_shared<CappedFlooredIborCoupon>(
                paymentDate, nominal, startDate, endDate, fixingDays, index,
                gearing, spread, c, f, refPeriodStart, refPeriodEnd,
                dc, isInArrears, exCouponDate);
        }),
            py::arg("paymentDate"), py::arg("nominal"),
            py::arg("startDate"), py::arg("endDate"),
            py::arg("fixingDays"), py::arg("index"),
            py::arg("gearing") = 1.0, py::arg("spread") = 0.0,
            py::arg("cap") = py::none(), py::arg("floor") = py::none(),
            py::arg("refPeriodStart") = Date(), py::arg("refPeriodEnd") = Date(),
            py::arg("dayCounter") = py::none(),
            py::arg("isInArrears") = false, py::arg("exCouponDate") = Date(),
            "Constructs a capped/floored Ibor coupon.");

    // CappedFlooredCmsCoupon
    py::class_<CappedFlooredCmsCoupon, CappedFlooredCoupon,
               ext::shared_ptr<CappedFlooredCmsCoupon>>(
        m, "CappedFlooredCmsCoupon",
        "Capped/floored CMS coupon.")
        .def(py::init([](const Date& paymentDate, Real nominal,
                         const Date& startDate, const Date& endDate,
                         Natural fixingDays,
                         const ext::shared_ptr<SwapIndex>& index,
                         Real gearing, Spread spread,
                         const py::object& cap, const py::object& floor,
                         const Date& refPeriodStart, const Date& refPeriodEnd,
                         const py::object& dayCounter,
                         bool isInArrears, const Date& exCouponDate) {
            Rate c = cap.is_none() ? Null<Rate>() : cap.cast<Rate>();
            Rate f = floor.is_none() ? Null<Rate>() : floor.cast<Rate>();
            DayCounter dc;
            if (!dayCounter.is_none())
                dc = dayCounter.cast<DayCounter>();
            return ext::make_shared<CappedFlooredCmsCoupon>(
                paymentDate, nominal, startDate, endDate, fixingDays, index,
                gearing, spread, c, f, refPeriodStart, refPeriodEnd,
                dc, isInArrears, exCouponDate);
        }),
            py::arg("paymentDate"), py::arg("nominal"),
            py::arg("startDate"), py::arg("endDate"),
            py::arg("fixingDays"), py::arg("index"),
            py::arg("gearing") = 1.0, py::arg("spread") = 0.0,
            py::arg("cap") = py::none(), py::arg("floor") = py::none(),
            py::arg("refPeriodStart") = Date(), py::arg("refPeriodEnd") = Date(),
            py::arg("dayCounter") = py::none(),
            py::arg("isInArrears") = false, py::arg("exCouponDate") = Date(),
            "Constructs a capped/floored CMS coupon.");
}
