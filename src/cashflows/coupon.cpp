/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 *
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 *
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */

#include "pyquantlib/pyquantlib.h"
#include "pyquantlib/trampolines.h"
#include <ql/cashflows/coupon.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::coupon(py::module_& m) {
    py::class_<Coupon, PyCoupon, ext::shared_ptr<Coupon>, CashFlow>(m, "Coupon",
        "Abstract base class for coupon payments.")
        .def(py::init_alias<>())
        .def("date", &Coupon::date,
            "Returns the payment date.")
        .def("nominal", &Coupon::nominal,
            "Returns the nominal amount.")
        .def("rate", &Coupon::rate,
            "Returns the accrual rate.")
        .def("dayCounter", &Coupon::dayCounter,
            py::return_value_policy::reference_internal,
            "Returns the day counter.")
        .def("accrualStartDate", &Coupon::accrualStartDate,
            "Returns the accrual start date.")
        .def("accrualEndDate", &Coupon::accrualEndDate,
            "Returns the accrual end date.")
        .def("referencePeriodStart", &Coupon::referencePeriodStart,
            "Returns the reference period start date.")
        .def("referencePeriodEnd", &Coupon::referencePeriodEnd,
            "Returns the reference period end date.")
        .def("accrualPeriod", &Coupon::accrualPeriod,
            "Returns the accrual period as a year fraction.")
        .def("accrualDays", &Coupon::accrualDays,
            "Returns the number of accrual days.")
        .def("accruedAmount", &Coupon::accruedAmount,
            py::arg("date"),
            "Returns the accrued amount at the given date.");
}
