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
#include <ql/pricingengines/credit/isdacdsengine.hpp>
#include <ql/termstructures/defaulttermstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::isdacdsengine(py::module_& m) {
    // IsdaCdsEngine enums
    py::enum_<IsdaCdsEngine::NumericalFix>(m, "IsdaNumericalFix",
        "ISDA CDS engine numerical fix.")
        .value("IsdaNone", IsdaCdsEngine::None, "No fix.")
        .value("Taylor", IsdaCdsEngine::Taylor, "Taylor expansion fix.");

    py::enum_<IsdaCdsEngine::AccrualBias>(m, "IsdaAccrualBias",
        "ISDA CDS engine accrual bias.")
        .value("HalfDayBias", IsdaCdsEngine::HalfDayBias,
            "Half day bias.")
        .value("NoBias", IsdaCdsEngine::NoBias, "No bias.");

    py::enum_<IsdaCdsEngine::ForwardsInCouponPeriod>(
        m, "IsdaForwardsInCouponPeriod",
        "ISDA CDS forwards in coupon period.")
        .value("Flat", IsdaCdsEngine::Flat, "Flat forwards.")
        .value("Piecewise", IsdaCdsEngine::Piecewise,
            "Piecewise forwards.");

    py::class_<IsdaCdsEngine, PricingEngine,
               ext::shared_ptr<IsdaCdsEngine>>(
        m, "IsdaCdsEngine",
        "ISDA-compliant CDS engine.")
        // Handle constructor
        .def(py::init<Handle<DefaultProbabilityTermStructure>,
                       Real, Handle<YieldTermStructure>,
                       const ext::optional<bool>&,
                       IsdaCdsEngine::NumericalFix,
                       IsdaCdsEngine::AccrualBias,
                       IsdaCdsEngine::ForwardsInCouponPeriod>(),
            py::arg("probability"),
            py::arg("recoveryRate"),
            py::arg("discountCurve"),
            py::arg("includeSettlementDateFlows") = ext::nullopt,
            py::arg("numericalFix") = IsdaCdsEngine::Taylor,
            py::arg("accrualBias") = IsdaCdsEngine::HalfDayBias,
            py::arg("forwardsInCouponPeriod") = IsdaCdsEngine::Piecewise,
            "Constructs from handles.")
        // Hidden handle: shared_ptr convenience
        .def(py::init([](const ext::shared_ptr<DefaultProbabilityTermStructure>& prob,
                         Real recoveryRate,
                         const ext::shared_ptr<YieldTermStructure>& disc,
                         const ext::optional<bool>& settle,
                         IsdaCdsEngine::NumericalFix numericalFix,
                         IsdaCdsEngine::AccrualBias accrualBias,
                         IsdaCdsEngine::ForwardsInCouponPeriod fwds) {
            return ext::make_shared<IsdaCdsEngine>(
                Handle<DefaultProbabilityTermStructure>(prob),
                recoveryRate,
                Handle<YieldTermStructure>(disc),
                settle, numericalFix, accrualBias, fwds);
        }),
            py::arg("probability"),
            py::arg("recoveryRate"),
            py::arg("discountCurve"),
            py::arg("includeSettlementDateFlows") = ext::nullopt,
            py::arg("numericalFix") = IsdaCdsEngine::Taylor,
            py::arg("accrualBias") = IsdaCdsEngine::HalfDayBias,
            py::arg("forwardsInCouponPeriod") = IsdaCdsEngine::Piecewise,
            "Constructs from term structures (handles created internally).")
        .def("isdaRateCurve", &IsdaCdsEngine::isdaRateCurve,
            "ISDA rate curve.")
        .def("isdaCreditCurve", &IsdaCdsEngine::isdaCreditCurve,
            "ISDA credit curve.");
}
