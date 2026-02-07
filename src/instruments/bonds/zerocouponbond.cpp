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
#include <ql/instruments/bonds/zerocouponbond.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::zerocouponbond(py::module_& m) {
    py::class_<ZeroCouponBond, Bond, ext::shared_ptr<ZeroCouponBond>>(
        m, "ZeroCouponBond",
        "Zero coupon bond.")
        .def(py::init<Natural, const Calendar&, Real, const Date&,
                       BusinessDayConvention, Real, const Date&>(),
            py::arg("settlementDays"),
            py::arg("calendar"),
            py::arg("faceAmount"),
            py::arg("maturityDate"),
            py::arg("paymentConvention") = Following,
            py::arg("redemption") = 100.0,
            py::arg("issueDate") = Date(),
            "Constructs a zero coupon bond.");
}
