/*
 * PyQuantLib: Python bindings for QuantLib
 * https://github.com/quantales/pyquantlib
 *
 * Copyright (c) 2025 Yassine Idyiahia
 * SPDX-License-Identifier: BSD-3-Clause
 * See LICENSE for details.
 *
 * ---
 * QuantLib is free software distributed under its own modified BSD license,
 * and is copyright of its respective contributors.
 * https://www.quantlib.org/
 */

#include "pyquantlib/pyquantlib.h"
#include <ql/pricingengines/futures/discountingperpetualfuturesengine.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::discountingperpetualfuturesengine(py::module_& m) {
    py::class_<DiscountingPerpetualFuturesEngine, PricingEngine,
               ext::shared_ptr<DiscountingPerpetualFuturesEngine>>
        cls(m, "DiscountingPerpetualFuturesEngine",
            "Discounting engine for perpetual futures (Ackerer, Hugonnier, "
            "Jermann, 2024).");

    py::enum_<DiscountingPerpetualFuturesEngine::InterpolationType>(
        cls, "InterpolationType",
        "Interpolation applied to the funding-rate term structure.")
        .value("PiecewiseConstant",
               DiscountingPerpetualFuturesEngine::PiecewiseConstant)
        .value("Linear", DiscountingPerpetualFuturesEngine::Linear)
        .value("CubicSpline", DiscountingPerpetualFuturesEngine::CubicSpline)
        .export_values();

    cls.def(py::init<const Handle<YieldTermStructure>&,
                     const Handle<YieldTermStructure>&, const Handle<Quote>&,
                     const std::vector<Time>&, const std::vector<Rate>&,
                     const std::vector<Spread>&,
                     DiscountingPerpetualFuturesEngine::InterpolationType,
                     Real>(),
            py::arg("domesticDiscountCurve"),
            py::arg("foreignDiscountCurve"),
            py::arg("assetSpot"),
            py::arg("fundingTimes"),
            py::arg("fundingRates"),
            py::arg("interestRateDiffs"),
            py::arg("fundingInterpType") =
                DiscountingPerpetualFuturesEngine::PiecewiseConstant,
            py::arg("maxT") = 60.0,
            "Constructs the engine from discount curves, spot, and the "
            "funding-rate schedule.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& domestic,
                         const ext::shared_ptr<YieldTermStructure>& foreign,
                         const ext::shared_ptr<Quote>& assetSpot,
                         const std::vector<Time>& fundingTimes,
                         const std::vector<Rate>& fundingRates,
                         const std::vector<Spread>& interestRateDiffs,
                         DiscountingPerpetualFuturesEngine::InterpolationType
                             fundingInterpType,
                         Real maxT) {
            return ext::make_shared<DiscountingPerpetualFuturesEngine>(
                Handle<YieldTermStructure>(domestic),
                Handle<YieldTermStructure>(foreign), Handle<Quote>(assetSpot),
                fundingTimes, fundingRates, interestRateDiffs,
                fundingInterpType, maxT);
        }),
            py::arg("domesticDiscountCurve"),
            py::arg("foreignDiscountCurve"),
            py::arg("assetSpot"),
            py::arg("fundingTimes"),
            py::arg("fundingRates"),
            py::arg("interestRateDiffs"),
            py::arg("fundingInterpType") =
                DiscountingPerpetualFuturesEngine::PiecewiseConstant,
            py::arg("maxT") = 60.0,
            "Constructs the engine (handles created internally).")
        .def("domesticDiscountCurve",
             &DiscountingPerpetualFuturesEngine::domesticDiscountCurve,
             "Returns the domestic discount curve.")
        .def("foreignDiscountCurve",
             &DiscountingPerpetualFuturesEngine::foreignDiscountCurve,
             "Returns the foreign discount curve.")
        .def("assetSpot", &DiscountingPerpetualFuturesEngine::assetSpot,
             "Returns the asset spot quote.")
        .def("fundingTimes", &DiscountingPerpetualFuturesEngine::fundingTimes,
             "Returns the funding-time grid.")
        .def("fundingRates", &DiscountingPerpetualFuturesEngine::fundingRates,
             "Returns the funding rates.")
        .def("interestRateDiffs",
             &DiscountingPerpetualFuturesEngine::interestRateDiffs,
             "Returns the interest-rate differentials.");
}
