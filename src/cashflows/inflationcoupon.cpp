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
#include <ql/cashflows/inflationcoupon.hpp>
#include <ql/cashflows/inflationcouponpricer.hpp>
#include <ql/indexes/inflationindex.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::inflationcoupon(py::module_& m) {
    py::class_<InflationCoupon, Coupon, ext::shared_ptr<InflationCoupon>>(
        m, "InflationCoupon",
        "Abstract base class for inflation coupons.")
        // Inspectors
        .def("index", &InflationCoupon::index,
            "Returns the inflation index.")
        .def("observationLag", &InflationCoupon::observationLag,
            "Returns the observation lag.")
        .def("fixingDays", &InflationCoupon::fixingDays,
            "Returns the number of fixing days.")
        .def("fixingDate", &InflationCoupon::fixingDate,
            "Returns the fixing date.")
        .def("indexFixing", &InflationCoupon::indexFixing,
            "Returns the index fixing.")
        .def("dayCounter", &InflationCoupon::dayCounter,
            "Returns the day counter.")
        .def("rate", &InflationCoupon::rate,
            "Returns the coupon rate.")
        .def("accruedAmount", &InflationCoupon::accruedAmount,
            py::arg("date"),
            "Returns the accrued amount at the given date.")
        .def("amount", &InflationCoupon::amount,
            "Returns the coupon amount.")
        .def("price", &InflationCoupon::price,
            py::arg("discountingCurve"),
            "Returns the present value given a discounting curve.")
        // Pricer
        .def("setPricer", &InflationCoupon::setPricer,
            py::arg("pricer"),
            "Sets the inflation coupon pricer.")
        .def("pricer", &InflationCoupon::pricer,
            "Returns the inflation coupon pricer.");
}
