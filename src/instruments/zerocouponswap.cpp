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
#include <ql/instruments/zerocouponswap.hpp>
#include <ql/indexes/iborindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::zerocouponswap(py::module_& m) {
    py::class_<ZeroCouponSwap, Swap, ext::shared_ptr<ZeroCouponSwap>>(
        m, "ZeroCouponSwap",
        "Zero-coupon interest rate swap.")
        // Constructor: fixed payment amount
        .def(py::init<Swap::Type, Real, const Date&, const Date&,
                       Real, ext::shared_ptr<IborIndex>,
                       const Calendar&, BusinessDayConvention, Natural>(),
            py::arg("type"),
            py::arg("baseNominal"),
            py::arg("startDate"),
            py::arg("maturityDate"),
            py::arg("fixedPayment"),
            py::arg("iborIndex"),
            py::arg("paymentCalendar"),
            py::arg("paymentConvention") = Following,
            py::arg("paymentDelay") = 0,
            "Constructs from fixed payment amount.")
        // Constructor: fixed rate
        .def(py::init<Swap::Type, Real, const Date&, const Date&,
                       Rate, const DayCounter&, ext::shared_ptr<IborIndex>,
                       const Calendar&, BusinessDayConvention, Natural>(),
            py::arg("type"),
            py::arg("baseNominal"),
            py::arg("startDate"),
            py::arg("maturityDate"),
            py::arg("fixedRate"),
            py::arg("fixedDayCounter"),
            py::arg("iborIndex"),
            py::arg("paymentCalendar"),
            py::arg("paymentConvention") = Following,
            py::arg("paymentDelay") = 0,
            "Constructs from fixed rate.")
        // Inspectors
        .def("type", &ZeroCouponSwap::type, "Swap type (payer or receiver).")
        .def("baseNominal", &ZeroCouponSwap::baseNominal,
            "Base notional amount.")
        .def("startDate", &ZeroCouponSwap::startDate, "Start date.")
        .def("maturityDate", &ZeroCouponSwap::maturityDate, "Maturity date.")
        .def("iborIndex", &ZeroCouponSwap::iborIndex, "Ibor index.")
        .def("fixedLeg", &ZeroCouponSwap::fixedLeg, "Fixed leg.")
        .def("floatingLeg", &ZeroCouponSwap::floatingLeg, "Floating leg.")
        .def("fixedPayment", &ZeroCouponSwap::fixedPayment,
            "Fixed payment amount.")
        // Results
        .def("fixedLegNPV", &ZeroCouponSwap::fixedLegNPV,
            "NPV of the fixed leg.")
        .def("floatingLegNPV", &ZeroCouponSwap::floatingLegNPV,
            "NPV of the floating leg.")
        .def("fairFixedPayment", &ZeroCouponSwap::fairFixedPayment,
            "Fair fixed payment amount.")
        .def("fairFixedRate", &ZeroCouponSwap::fairFixedRate,
            py::arg("dayCounter"),
            "Fair fixed rate for a given day counter.");
}
