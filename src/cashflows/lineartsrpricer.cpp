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
#include <ql/cashflows/lineartsrpricer.hpp>
#include <ql/cashflows/couponpricer.hpp>
#include <ql/termstructures/volatility/swaption/swaptionvolstructure.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::lineartsrpricer(py::module_& m) {
    using Settings = LinearTsrPricer::Settings;

    // Strategy enum
    py::enum_<Settings::Strategy>(m, "LinearTsrPricerStrategy",
        "Integration boundary determination strategy.")
        .value("RateBound", Settings::RateBound)
        .value("VegaRatio", Settings::VegaRatio)
        .value("PriceThreshold", Settings::PriceThreshold)
        .value("BSStdDevs", Settings::BSStdDevs);

    // Settings nested class
    py::class_<Settings>(m, "LinearTsrPricerSettings",
        "Settings for LinearTsrPricer integration bounds.")
        .def(py::init<>(), "Constructs default settings (RateBound strategy).")
        .def("withRateBound", &Settings::withRateBound,
            py::return_value_policy::reference_internal,
            py::arg("lowerRateBound") = 0.0,
            py::arg("upperRateBound") = 2.0,
            "Sets rate bound strategy with explicit bounds.")
        .def("withVegaRatio",
            py::overload_cast<Real>(&Settings::withVegaRatio),
            py::return_value_policy::reference_internal,
            py::arg("vegaRatio") = 0.01,
            "Sets vega ratio strategy with default bounds.")
        .def("withVegaRatio",
            py::overload_cast<Real, Real, Real>(&Settings::withVegaRatio),
            py::return_value_policy::reference_internal,
            py::arg("vegaRatio"), py::arg("lowerRateBound"),
            py::arg("upperRateBound"),
            "Sets vega ratio strategy with explicit bounds.")
        .def("withPriceThreshold",
            py::overload_cast<Real>(&Settings::withPriceThreshold),
            py::return_value_policy::reference_internal,
            py::arg("priceThreshold") = 1.0e-8,
            "Sets price threshold strategy with default bounds.")
        .def("withPriceThreshold",
            py::overload_cast<Real, Real, Real>(&Settings::withPriceThreshold),
            py::return_value_policy::reference_internal,
            py::arg("priceThreshold"), py::arg("lowerRateBound"),
            py::arg("upperRateBound"),
            "Sets price threshold strategy with explicit bounds.")
        .def("withBSStdDevs",
            py::overload_cast<Real>(&Settings::withBSStdDevs),
            py::return_value_policy::reference_internal,
            py::arg("stdDevs") = 3.0,
            "Sets Black-Scholes std devs strategy with default bounds.")
        .def("withBSStdDevs",
            py::overload_cast<Real, Real, Real>(&Settings::withBSStdDevs),
            py::return_value_policy::reference_internal,
            py::arg("stdDevs"), py::arg("lowerRateBound"),
            py::arg("upperRateBound"),
            "Sets Black-Scholes std devs strategy with explicit bounds.");

    // LinearTsrPricer
    py::class_<LinearTsrPricer, CmsCouponPricer, MeanRevertingPricer,
               ext::shared_ptr<LinearTsrPricer>>(m, "LinearTsrPricer",
        "CMS coupon pricer using linear terminal swap rate model.")
        // Explicit handle constructor
        .def(py::init([](const Handle<SwaptionVolatilityStructure>& swaptionVol,
                         const Handle<Quote>& meanReversion,
                         const py::object& couponDiscountCurve,
                         const Settings& settings) {
            Handle<YieldTermStructure> cdc;
            if (!couponDiscountCurve.is_none())
                cdc = couponDiscountCurve.cast<Handle<YieldTermStructure>>();
            return ext::make_shared<LinearTsrPricer>(
                swaptionVol, meanReversion, cdc, settings);
        }),
            py::arg("swaptionVol"), py::arg("meanReversion"),
            py::arg("couponDiscountCurve") = py::none(),
            py::arg("settings") = Settings(),
            "Constructs with explicit handles.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<SwaptionVolatilityStructure>& swaptionVol,
                         const ext::shared_ptr<Quote>& meanReversion,
                         const py::object& couponDiscountCurve,
                         const Settings& settings) {
            Handle<YieldTermStructure> cdc;
            if (!couponDiscountCurve.is_none())
                cdc = Handle<YieldTermStructure>(
                    couponDiscountCurve.cast<ext::shared_ptr<YieldTermStructure>>());
            return ext::make_shared<LinearTsrPricer>(
                Handle<SwaptionVolatilityStructure>(swaptionVol),
                Handle<Quote>(meanReversion),
                cdc, settings);
        }),
            py::arg("swaptionVol"), py::arg("meanReversion"),
            py::arg("couponDiscountCurve") = py::none(),
            py::arg("settings") = Settings(),
            "Constructs from shared pointers (handles created internally).")
        .def("swapletPrice", &LinearTsrPricer::swapletPrice,
            "Returns the swaplet price.")
        .def("swapletRate", &LinearTsrPricer::swapletRate,
            "Returns the swaplet rate.")
        .def("capletPrice", &LinearTsrPricer::capletPrice,
            py::arg("effectiveCap"),
            "Returns the caplet price.")
        .def("capletRate", &LinearTsrPricer::capletRate,
            py::arg("effectiveCap"),
            "Returns the caplet rate.")
        .def("floorletPrice", &LinearTsrPricer::floorletPrice,
            py::arg("effectiveFloor"),
            "Returns the floorlet price.")
        .def("floorletRate", &LinearTsrPricer::floorletRate,
            py::arg("effectiveFloor"),
            "Returns the floorlet rate.")
        .def("meanReversion", &LinearTsrPricer::meanReversion,
            "Returns the mean reversion value.")
        .def("setMeanReversion", &LinearTsrPricer::setMeanReversion,
            py::arg("meanReversion"),
            "Sets the mean reversion handle.");
}
