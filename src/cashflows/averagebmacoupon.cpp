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
#include <ql/cashflows/averagebmacoupon.hpp>
#include <ql/indexes/bmaindex.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::averagebmacoupon(py::module_& m) {
    py::class_<AverageBMACoupon, FloatingRateCoupon,
               ext::shared_ptr<AverageBMACoupon>>(
        m, "AverageBMACoupon",
        "Coupon paying the weighted average of BMA fixings.")
        .def(py::init([](const Date& paymentDate, Real nominal,
                         const Date& startDate, const Date& endDate,
                         const ext::shared_ptr<BMAIndex>& index,
                         Real gearing, Spread spread,
                         const Date& refPeriodStart,
                         const Date& refPeriodEnd,
                         const py::object& dayCounter) {
            DayCounter dc;
            if (!dayCounter.is_none())
                dc = dayCounter.cast<DayCounter>();
            return ext::make_shared<AverageBMACoupon>(
                paymentDate, nominal, startDate, endDate,
                index, gearing, spread,
                refPeriodStart, refPeriodEnd, dc);
        }),
            py::arg("paymentDate"),
            py::arg("nominal"),
            py::arg("startDate"),
            py::arg("endDate"),
            py::arg("index"),
            py::arg("gearing") = 1.0,
            py::arg("spread") = 0.0,
            py::arg("refPeriodStart") = Date(),
            py::arg("refPeriodEnd") = Date(),
            py::arg("dayCounter") = py::none(),
            "Constructs an average BMA coupon.")
        .def("fixingDates", &AverageBMACoupon::fixingDates,
            "Returns the fixing dates to be averaged.")
        .def("indexFixings", &AverageBMACoupon::indexFixings,
            "Returns the index fixings to be averaged.");

    // AverageBMALeg builder
    py::class_<AverageBMALeg>(
        m, "AverageBMALeg",
        "Builder for a sequence of average BMA coupons.")
        .def(py::init<Schedule, ext::shared_ptr<BMAIndex>>(),
            py::arg("schedule"), py::arg("index"),
            "Constructs an AverageBMALeg builder.")
        .def("withNotionals",
            py::overload_cast<Real>(&AverageBMALeg::withNotionals),
            py::arg("notional"),
            py::return_value_policy::reference_internal,
            "Sets a single notional.")
        .def("withNotionals",
            py::overload_cast<const std::vector<Real>&>(
                &AverageBMALeg::withNotionals),
            py::arg("notionals"),
            py::return_value_policy::reference_internal,
            "Sets notional schedule.")
        .def("withPaymentDayCounter",
            &AverageBMALeg::withPaymentDayCounter,
            py::arg("dayCounter"),
            py::return_value_policy::reference_internal,
            "Sets payment day counter.")
        .def("withPaymentAdjustment",
            &AverageBMALeg::withPaymentAdjustment,
            py::arg("convention"),
            py::return_value_policy::reference_internal,
            "Sets payment business day convention.")
        .def("withGearings",
            py::overload_cast<Real>(&AverageBMALeg::withGearings),
            py::arg("gearing"),
            py::return_value_policy::reference_internal,
            "Sets a single gearing.")
        .def("withGearings",
            py::overload_cast<const std::vector<Real>&>(
                &AverageBMALeg::withGearings),
            py::arg("gearings"),
            py::return_value_policy::reference_internal,
            "Sets gearing schedule.")
        .def("withSpreads",
            py::overload_cast<Spread>(&AverageBMALeg::withSpreads),
            py::arg("spread"),
            py::return_value_policy::reference_internal,
            "Sets a single spread.")
        .def("withSpreads",
            py::overload_cast<const std::vector<Spread>&>(
                &AverageBMALeg::withSpreads),
            py::arg("spreads"),
            py::return_value_policy::reference_internal,
            "Sets spread schedule.")
        .def("leg", [](const AverageBMALeg& builder) -> Leg {
            return static_cast<Leg>(builder);
        }, "Builds and returns the leg.");
}
