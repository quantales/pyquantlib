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
#include <ql/experimental/callablebonds/callablebond.hpp>
#include <ql/time/schedule.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_experimental::callablebond(py::module_& m) {
    auto base = py::module_::import("pyquantlib.base");

    // CallableBond (abstract, protected constructor)
    auto pyCallableBond = py::class_<CallableBond, Bond, ext::shared_ptr<CallableBond>>(
        base, "CallableBond",
        "Callable bond base class.")
        // Inspectors
        .def("callability", &CallableBond::callability,
            py::return_value_policy::reference_internal,
            "Returns the put/call schedule.")
        // Calculations
        .def("impliedVolatility", &CallableBond::impliedVolatility,
            py::arg("targetPrice"),
            py::arg("discountCurve"),
            py::arg("accuracy"),
            py::arg("maxEvaluations"),
            py::arg("minVol"),
            py::arg("maxVol"),
            "Returns the Black implied forward yield volatility.")
        .def("OAS", &CallableBond::OAS,
            py::arg("cleanPrice"),
            py::arg("engineTS"),
            py::arg("dayCounter"),
            py::arg("compounding"),
            py::arg("frequency"),
            py::arg("settlementDate") = Date(),
            py::arg("accuracy") = 1.0e-10,
            py::arg("maxIterations") = 100,
            py::arg("guess") = 0.0,
            "Returns the option-adjusted spread.")
        .def("cleanPriceOAS", &CallableBond::cleanPriceOAS,
            py::arg("oas"),
            py::arg("engineTS"),
            py::arg("dayCounter"),
            py::arg("compounding"),
            py::arg("frequency"),
            py::arg("settlementDate") = Date(),
            "Returns the clean price given an OAS.")
        .def("effectiveDuration", &CallableBond::effectiveDuration,
            py::arg("oas"),
            py::arg("engineTS"),
            py::arg("dayCounter"),
            py::arg("compounding"),
            py::arg("frequency"),
            py::arg("bump") = 2e-4,
            "Returns the effective duration.")
        .def("effectiveConvexity", &CallableBond::effectiveConvexity,
            py::arg("oas"),
            py::arg("engineTS"),
            py::arg("dayCounter"),
            py::arg("compounding"),
            py::arg("frequency"),
            py::arg("bump") = 2e-4,
            "Returns the effective convexity.");

    // CallableFixedRateBond
    py::class_<CallableFixedRateBond, CallableBond, ext::shared_ptr<CallableFixedRateBond>>(
        m, "CallableFixedRateBond",
        "Callable/puttable fixed rate bond.")
        .def(py::init([](Natural settlementDays, Real faceAmount,
                         Schedule schedule,
                         const std::vector<Rate>& coupons,
                         const DayCounter& accrualDayCounter,
                         BusinessDayConvention paymentConvention,
                         Real redemption,
                         const Date& issueDate,
                         const CallabilitySchedule& putCallSchedule) {
            return ext::make_shared<CallableFixedRateBond>(
                settlementDays, faceAmount, std::move(schedule), coupons,
                accrualDayCounter, paymentConvention, redemption,
                issueDate, putCallSchedule);
        }),
            py::arg("settlementDays"),
            py::arg("faceAmount"),
            py::arg("schedule"),
            py::arg("coupons"),
            py::arg("accrualDayCounter"),
            py::arg("paymentConvention") = Following,
            py::arg("redemption") = 100.0,
            py::arg("issueDate") = Date(),
            py::arg("putCallSchedule") = CallabilitySchedule(),
            "Constructs a callable fixed rate bond.");

    // CallableZeroCouponBond
    py::class_<CallableZeroCouponBond, CallableBond, ext::shared_ptr<CallableZeroCouponBond>>(
        m, "CallableZeroCouponBond",
        "Callable/puttable zero coupon bond.")
        .def(py::init([](Natural settlementDays, Real faceAmount,
                         const Calendar& calendar, const Date& maturityDate,
                         const DayCounter& dayCounter,
                         BusinessDayConvention paymentConvention,
                         Real redemption, const Date& issueDate,
                         const CallabilitySchedule& putCallSchedule) {
            return ext::make_shared<CallableZeroCouponBond>(
                settlementDays, faceAmount, calendar, maturityDate,
                dayCounter, paymentConvention, redemption,
                issueDate, putCallSchedule);
        }),
            py::arg("settlementDays"),
            py::arg("faceAmount"),
            py::arg("calendar"),
            py::arg("maturityDate"),
            py::arg("dayCounter"),
            py::arg("paymentConvention") = Following,
            py::arg("redemption") = 100.0,
            py::arg("issueDate") = Date(),
            py::arg("putCallSchedule") = CallabilitySchedule(),
            "Constructs a callable zero coupon bond.");
}
