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
#include <ql/cashflows/conundrumpricer.hpp>
#include <ql/termstructures/volatility/swaption/swaptionvolstructure.hpp>
#include <ql/quote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::conundrumpricer(py::module_& m) {
    // GFunctionFactory::YieldCurveModel enum
    py::enum_<GFunctionFactory::YieldCurveModel>(m, "YieldCurveModel",
        "Yield curve model for CMS convexity adjustment.")
        .value("Standard", GFunctionFactory::Standard)
        .value("ExactYield", GFunctionFactory::ExactYield)
        .value("ParallelShifts", GFunctionFactory::ParallelShifts)
        .value("NonParallelShifts", GFunctionFactory::NonParallelShifts);

    // HaganPricer ABC
    py::class_<HaganPricer, CmsCouponPricer, MeanRevertingPricer,
               ext::shared_ptr<HaganPricer>>(
        m, "HaganPricer",
        "CMS coupon pricer using Hagan static replication.")
        .def("swapletRate", &HaganPricer::swapletRate,
            "Returns the swaplet rate.")
        .def("capletPrice", &HaganPricer::capletPrice,
            py::arg("effectiveCap"),
            "Returns the caplet price.")
        .def("capletRate", &HaganPricer::capletRate,
            py::arg("effectiveCap"),
            "Returns the caplet rate.")
        .def("floorletPrice", &HaganPricer::floorletPrice,
            py::arg("effectiveFloor"),
            "Returns the floorlet price.")
        .def("floorletRate", &HaganPricer::floorletRate,
            py::arg("effectiveFloor"),
            "Returns the floorlet rate.")
        .def("meanReversion", &HaganPricer::meanReversion,
            "Returns the mean reversion value.")
        .def("setMeanReversion", &HaganPricer::setMeanReversion,
            py::arg("meanReversion"),
            "Sets the mean reversion handle.");

    // AnalyticHaganPricer
    py::class_<AnalyticHaganPricer, HaganPricer,
               ext::shared_ptr<AnalyticHaganPricer>>(
        m, "AnalyticHaganPricer",
        "Analytic CMS coupon pricer using Hagan formula.")
        // Explicit handle constructor
        .def(py::init<const Handle<SwaptionVolatilityStructure>&,
                      GFunctionFactory::YieldCurveModel,
                      const Handle<Quote>&>(),
            py::arg("swaptionVol"), py::arg("modelOfYieldCurve"),
            py::arg("meanReversion"),
            "Constructs with explicit handles.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<SwaptionVolatilityStructure>& swaptionVol,
                         GFunctionFactory::YieldCurveModel modelOfYieldCurve,
                         const ext::shared_ptr<Quote>& meanReversion) {
            return ext::make_shared<AnalyticHaganPricer>(
                Handle<SwaptionVolatilityStructure>(swaptionVol),
                modelOfYieldCurve,
                Handle<Quote>(meanReversion));
        }),
            py::arg("swaptionVol"), py::arg("modelOfYieldCurve"),
            py::arg("meanReversion"),
            "Constructs from shared pointers (handles created internally).");

    // NumericHaganPricer
    py::class_<NumericHaganPricer, HaganPricer,
               ext::shared_ptr<NumericHaganPricer>>(
        m, "NumericHaganPricer",
        "Numeric CMS coupon pricer using Hagan integration.")
        // Explicit handle constructor
        .def(py::init<const Handle<SwaptionVolatilityStructure>&,
                      GFunctionFactory::YieldCurveModel,
                      const Handle<Quote>&,
                      Rate, Rate, Real, Real>(),
            py::arg("swaptionVol"), py::arg("modelOfYieldCurve"),
            py::arg("meanReversion"),
            py::arg("lowerLimit") = 0.0,
            py::arg("upperLimit") = 1.0,
            py::arg("precision") = 1.0e-6,
            py::arg("hardUpperLimit") = QL_MAX_REAL,
            "Constructs with explicit handles.")
        // Hidden handle constructor
        .def(py::init([](const ext::shared_ptr<SwaptionVolatilityStructure>& swaptionVol,
                         GFunctionFactory::YieldCurveModel modelOfYieldCurve,
                         const ext::shared_ptr<Quote>& meanReversion,
                         Rate lowerLimit, Rate upperLimit,
                         Real precision, Real hardUpperLimit) {
            return ext::make_shared<NumericHaganPricer>(
                Handle<SwaptionVolatilityStructure>(swaptionVol),
                modelOfYieldCurve,
                Handle<Quote>(meanReversion),
                lowerLimit, upperLimit, precision, hardUpperLimit);
        }),
            py::arg("swaptionVol"), py::arg("modelOfYieldCurve"),
            py::arg("meanReversion"),
            py::arg("lowerLimit") = 0.0,
            py::arg("upperLimit") = 1.0,
            py::arg("precision") = 1.0e-6,
            py::arg("hardUpperLimit") = QL_MAX_REAL,
            "Constructs from shared pointers (handles created internally).")
        .def("upperLimit", &NumericHaganPricer::upperLimit,
            "Returns the upper integration limit.")
        .def("lowerLimit", &NumericHaganPricer::lowerLimit,
            "Returns the lower integration limit.")
        .def("stdDeviations", &NumericHaganPricer::stdDeviations,
            "Returns the number of standard deviations for upper limit.");
}
