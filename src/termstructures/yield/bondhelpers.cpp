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
#include <ql/termstructures/yield/bondhelpers.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

// Bond::Price::Type is bound in instruments (later module), so use py::none()
// sentinel with default = Clean to avoid "type not registered yet" errors.
static Bond::Price::Type parsePriceType(const py::object& obj) {
    if (obj.is_none())
        return Bond::Price::Clean;
    return obj.cast<Bond::Price::Type>();
}

void ql_termstructures::bondhelpers(py::module_& m) {
    // --- BondHelper ---
    py::class_<BondHelper, RateHelper, ext::shared_ptr<BondHelper>>(
        m, "BondHelper",
        "Bond helper for bootstrapping yield curves.")
        // Handle<Quote> + Bond
        .def(py::init([](const Handle<Quote>& price,
                         const ext::shared_ptr<Bond>& bond,
                         const py::object& priceType) {
            return ext::make_shared<BondHelper>(
                price, bond, parsePriceType(priceType));
        }), py::arg("price"), py::arg("bond"),
            py::arg("priceType") = py::none(),
            "Constructs from price handle and bond.")
        // shared_ptr<Quote> + Bond (hidden handle)
        .def(py::init([](const ext::shared_ptr<Quote>& price,
                         const ext::shared_ptr<Bond>& bond,
                         const py::object& priceType) {
            return ext::make_shared<BondHelper>(
                Handle<Quote>(price), bond, parsePriceType(priceType));
        }), py::arg("price"), py::arg("bond"),
            py::arg("priceType") = py::none(),
            "Constructs from quote and bond (handle created internally).")
        .def("bond", &BondHelper::bond,
            "Returns the underlying bond.")
        .def("priceType", &BondHelper::priceType,
            "Returns the price type (Clean or Dirty).");

    // --- FixedRateBondHelper ---
    py::class_<FixedRateBondHelper, BondHelper,
               ext::shared_ptr<FixedRateBondHelper>>(
        m, "FixedRateBondHelper",
        "Fixed-coupon bond helper for bootstrapping yield curves.")
        // Handle<Quote>
        .def(py::init([](const Handle<Quote>& price,
                         Natural settlementDays,
                         Real faceAmount,
                         Schedule schedule,
                         const std::vector<Rate>& coupons,
                         const DayCounter& dayCounter,
                         BusinessDayConvention paymentConv,
                         Real redemption,
                         const Date& issueDate,
                         const py::object& paymentCalendar,
                         const Period& exCouponPeriod,
                         const py::object& exCouponCalendar,
                         BusinessDayConvention exCouponConvention,
                         bool exCouponEndOfMonth,
                         const py::object& priceType) {
            Calendar payCal;
            if (!paymentCalendar.is_none())
                payCal = paymentCalendar.cast<Calendar>();
            Calendar exCal;
            if (!exCouponCalendar.is_none())
                exCal = exCouponCalendar.cast<Calendar>();
            return ext::make_shared<FixedRateBondHelper>(
                price, settlementDays, faceAmount, std::move(schedule),
                coupons, dayCounter, paymentConv, redemption, issueDate,
                payCal, exCouponPeriod, exCal,
                exCouponConvention, exCouponEndOfMonth,
                parsePriceType(priceType));
        }),
            py::arg("price"),
            py::arg("settlementDays"),
            py::arg("faceAmount"),
            py::arg("schedule"),
            py::arg("coupons"),
            py::arg("dayCounter"),
            py::arg("paymentConvention") = Following,
            py::arg("redemption") = 100.0,
            py::arg("issueDate") = Date(),
            py::arg("paymentCalendar") = py::none(),
            py::arg("exCouponPeriod") = Period(),
            py::arg("exCouponCalendar") = py::none(),
            py::arg("exCouponConvention") = Unadjusted,
            py::arg("exCouponEndOfMonth") = false,
            py::arg("priceType") = py::none(),
            "Constructs from price handle and bond parameters.")
        // shared_ptr<Quote> (hidden handle)
        .def(py::init([](const ext::shared_ptr<Quote>& price,
                         Natural settlementDays,
                         Real faceAmount,
                         Schedule schedule,
                         const std::vector<Rate>& coupons,
                         const DayCounter& dayCounter,
                         BusinessDayConvention paymentConv,
                         Real redemption,
                         const Date& issueDate,
                         const py::object& paymentCalendar,
                         const Period& exCouponPeriod,
                         const py::object& exCouponCalendar,
                         BusinessDayConvention exCouponConvention,
                         bool exCouponEndOfMonth,
                         const py::object& priceType) {
            Calendar payCal;
            if (!paymentCalendar.is_none())
                payCal = paymentCalendar.cast<Calendar>();
            Calendar exCal;
            if (!exCouponCalendar.is_none())
                exCal = exCouponCalendar.cast<Calendar>();
            return ext::make_shared<FixedRateBondHelper>(
                Handle<Quote>(price), settlementDays, faceAmount,
                std::move(schedule), coupons, dayCounter, paymentConv,
                redemption, issueDate, payCal, exCouponPeriod, exCal,
                exCouponConvention, exCouponEndOfMonth,
                parsePriceType(priceType));
        }),
            py::arg("price"),
            py::arg("settlementDays"),
            py::arg("faceAmount"),
            py::arg("schedule"),
            py::arg("coupons"),
            py::arg("dayCounter"),
            py::arg("paymentConvention") = Following,
            py::arg("redemption") = 100.0,
            py::arg("issueDate") = Date(),
            py::arg("paymentCalendar") = py::none(),
            py::arg("exCouponPeriod") = Period(),
            py::arg("exCouponCalendar") = py::none(),
            py::arg("exCouponConvention") = Unadjusted,
            py::arg("exCouponEndOfMonth") = false,
            py::arg("priceType") = py::none(),
            "Constructs from quote and bond parameters (handle created internally).")
        // Rate scalar (convenience)
        .def(py::init([](Real price,
                         Natural settlementDays,
                         Real faceAmount,
                         Schedule schedule,
                         const std::vector<Rate>& coupons,
                         const DayCounter& dayCounter,
                         BusinessDayConvention paymentConv,
                         Real redemption,
                         const Date& issueDate,
                         const py::object& paymentCalendar,
                         const Period& exCouponPeriod,
                         const py::object& exCouponCalendar,
                         BusinessDayConvention exCouponConvention,
                         bool exCouponEndOfMonth,
                         const py::object& priceType) {
            Calendar payCal;
            if (!paymentCalendar.is_none())
                payCal = paymentCalendar.cast<Calendar>();
            Calendar exCal;
            if (!exCouponCalendar.is_none())
                exCal = exCouponCalendar.cast<Calendar>();
            auto quote = ext::make_shared<SimpleQuote>(price);
            return ext::make_shared<FixedRateBondHelper>(
                Handle<Quote>(quote), settlementDays, faceAmount,
                std::move(schedule), coupons, dayCounter, paymentConv,
                redemption, issueDate, payCal, exCouponPeriod, exCal,
                exCouponConvention, exCouponEndOfMonth,
                parsePriceType(priceType));
        }),
            py::arg("price"),
            py::arg("settlementDays"),
            py::arg("faceAmount"),
            py::arg("schedule"),
            py::arg("coupons"),
            py::arg("dayCounter"),
            py::arg("paymentConvention") = Following,
            py::arg("redemption") = 100.0,
            py::arg("issueDate") = Date(),
            py::arg("paymentCalendar") = py::none(),
            py::arg("exCouponPeriod") = Period(),
            py::arg("exCouponCalendar") = py::none(),
            py::arg("exCouponConvention") = Unadjusted,
            py::arg("exCouponEndOfMonth") = false,
            py::arg("priceType") = py::none(),
            "Constructs from price value and bond parameters.");
}
