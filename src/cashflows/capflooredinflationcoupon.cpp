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
#include <ql/cashflows/capflooredinflationcoupon.hpp>
#include <ql/indexes/inflationindex.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::capflooredinflationcoupon(py::module_& m) {
    py::class_<CappedFlooredYoYInflationCoupon, YoYInflationCoupon,
               ext::shared_ptr<CappedFlooredYoYInflationCoupon>>(
        m, "CappedFlooredYoYInflationCoupon",
        "Capped and/or floored YoY inflation coupon.")
        // Constructor wrapping an underlying coupon
        .def(py::init([](const ext::shared_ptr<YoYInflationCoupon>& underlying,
                         const py::object& cap, const py::object& floor) {
                Rate c = cap.is_none() ? Null<Rate>() : cap.cast<Rate>();
                Rate f = floor.is_none() ? Null<Rate>() : floor.cast<Rate>();
                return ext::make_shared<CappedFlooredYoYInflationCoupon>(
                    underlying, c, f);
            }),
            py::arg("underlying"),
            py::arg("cap") = py::none(),
            py::arg("floor") = py::none(),
            "Constructs from an underlying YoY inflation coupon.")
        // Direct constructor
        .def(py::init([](const Date& paymentDate, Real nominal,
                         const Date& startDate, const Date& endDate,
                         Natural fixingDays,
                         const ext::shared_ptr<YoYInflationIndex>& index,
                         const Period& observationLag,
                         CPI::InterpolationType interpolation,
                         const DayCounter& dayCounter,
                         Real gearing, Spread spread,
                         const py::object& cap, const py::object& floor,
                         const Date& refPeriodStart,
                         const Date& refPeriodEnd) {
                Rate c = cap.is_none() ? Null<Rate>() : cap.cast<Rate>();
                Rate f = floor.is_none() ? Null<Rate>() : floor.cast<Rate>();
                return ext::make_shared<CappedFlooredYoYInflationCoupon>(
                    paymentDate, nominal, startDate, endDate, fixingDays,
                    index, observationLag, interpolation, dayCounter,
                    gearing, spread, c, f, refPeriodStart, refPeriodEnd);
            }),
            py::arg("paymentDate"),
            py::arg("nominal"),
            py::arg("startDate"),
            py::arg("endDate"),
            py::arg("fixingDays"),
            py::arg("index"),
            py::arg("observationLag"),
            py::arg("interpolation"),
            py::arg("dayCounter"),
            py::arg("gearing") = 1.0,
            py::arg("spread") = 0.0,
            py::arg("cap") = py::none(),
            py::arg("floor") = py::none(),
            py::arg("refPeriodStart") = Date(),
            py::arg("refPeriodEnd") = Date(),
            "Constructs a capped/floored YoY inflation coupon.")
        .def("cap", &CappedFlooredYoYInflationCoupon::cap,
            "Returns the cap rate.")
        .def("floor", &CappedFlooredYoYInflationCoupon::floor,
            "Returns the floor rate.")
        .def("effectiveCap", &CappedFlooredYoYInflationCoupon::effectiveCap,
            "Returns the effective cap of the fixing.")
        .def("effectiveFloor",
            &CappedFlooredYoYInflationCoupon::effectiveFloor,
            "Returns the effective floor of the fixing.")
        .def("isCapped", &CappedFlooredYoYInflationCoupon::isCapped,
            "Returns True if the coupon is capped.")
        .def("isFloored", &CappedFlooredYoYInflationCoupon::isFloored,
            "Returns True if the coupon is floored.");
}
