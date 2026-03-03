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
#include <ql/cashflows/digitalcoupon.hpp>
#include <ql/cashflows/couponpricer.hpp>
#include <ql/cashflows/replication.hpp>
#include <ql/position.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::digitalcoupon(py::module_& m) {
    py::class_<DigitalCoupon, FloatingRateCoupon,
               ext::shared_ptr<DigitalCoupon>>(
        m, "DigitalCoupon",
        "Floating-rate coupon with digital call/put option.")
        .def(py::init([](const ext::shared_ptr<FloatingRateCoupon>& underlying,
                         const py::object& callStrike,
                         Position::Type callPosition,
                         bool isCallITMIncluded,
                         const py::object& callDigitalPayoff,
                         const py::object& putStrike,
                         Position::Type putPosition,
                         bool isPutITMIncluded,
                         const py::object& putDigitalPayoff,
                         const py::object& replication,
                         bool nakedOption) {
            Rate cs = callStrike.is_none() ? Null<Rate>() : callStrike.cast<Rate>();
            Rate cp = callDigitalPayoff.is_none() ? Null<Rate>() : callDigitalPayoff.cast<Rate>();
            Rate ps = putStrike.is_none() ? Null<Rate>() : putStrike.cast<Rate>();
            Rate pp = putDigitalPayoff.is_none() ? Null<Rate>() : putDigitalPayoff.cast<Rate>();
            ext::shared_ptr<DigitalReplication> repl;
            if (!replication.is_none())
                repl = replication.cast<ext::shared_ptr<DigitalReplication>>();
            return ext::make_shared<DigitalCoupon>(
                underlying, cs, callPosition, isCallITMIncluded, cp,
                ps, putPosition, isPutITMIncluded, pp,
                repl, nakedOption);
        }),
            py::arg("underlying"),
            py::arg("callStrike") = py::none(),
            py::arg("callPosition") = Position::Long,
            py::arg("isCallITMIncluded") = false,
            py::arg("callDigitalPayoff") = py::none(),
            py::arg("putStrike") = py::none(),
            py::arg("putPosition") = Position::Long,
            py::arg("isPutITMIncluded") = false,
            py::arg("putDigitalPayoff") = py::none(),
            py::arg("replication") = py::none(),
            py::arg("nakedOption") = false,
            "Constructs a digital coupon.")
        .def("rate", &DigitalCoupon::rate,
            "Returns the coupon rate.")
        .def("convexityAdjustment", &DigitalCoupon::convexityAdjustment,
            "Returns the convexity adjustment.")
        .def("callStrike", &DigitalCoupon::callStrike,
            "Returns the call strike.")
        .def("putStrike", &DigitalCoupon::putStrike,
            "Returns the put strike.")
        .def("callDigitalPayoff", &DigitalCoupon::callDigitalPayoff,
            "Returns the call digital payoff.")
        .def("putDigitalPayoff", &DigitalCoupon::putDigitalPayoff,
            "Returns the put digital payoff.")
        .def("hasPut", &DigitalCoupon::hasPut,
            "Returns whether the coupon has a put.")
        .def("hasCall", &DigitalCoupon::hasCall,
            "Returns whether the coupon has a call.")
        .def("hasCollar", &DigitalCoupon::hasCollar,
            "Returns whether the coupon has a collar.")
        .def("isLongPut", &DigitalCoupon::isLongPut,
            "Returns whether the put position is long.")
        .def("isLongCall", &DigitalCoupon::isLongCall,
            "Returns whether the call position is long.")
        .def("underlying", &DigitalCoupon::underlying,
            "Returns the underlying floating-rate coupon.")
        .def("callOptionRate", &DigitalCoupon::callOptionRate,
            "Returns the call option rate.")
        .def("putOptionRate", &DigitalCoupon::putOptionRate,
            "Returns the put option rate.")
        .def("setPricer", &DigitalCoupon::setPricer,
            py::arg("pricer"),
            "Sets the coupon pricer.");
}
