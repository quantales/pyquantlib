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
#include <ql/cashflows/inflationcouponpricer.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/termstructures/volatility/inflation/yoyinflationoptionletvolatilitystructure.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_cashflows::inflationcouponpricer(py::module_& m) {
    auto base = py::module_::import("pyquantlib.base");

    // InflationCouponPricer ABC (base submodule)
    py::class_<InflationCouponPricer, ext::shared_ptr<InflationCouponPricer>,
               Observer, Observable>(base, "InflationCouponPricer",
        "Abstract base class for inflation coupon pricers.");

    // YoYInflationCouponPricer (concrete, main module)
    py::class_<YoYInflationCouponPricer, InflationCouponPricer,
               ext::shared_ptr<YoYInflationCouponPricer>>(
        m, "YoYInflationCouponPricer",
        "Base pricer for YoY inflation coupons.")
        .def(py::init<>(),
            "Constructs with no vol or nominal curve.")
        .def(py::init<Handle<YieldTermStructure>>(),
            py::arg("nominalTermStructure"),
            "Constructs with a nominal term structure.")
        .def(py::init<Handle<YoYOptionletVolatilitySurface>,
                       Handle<YieldTermStructure>>(),
            py::arg("capletVol"),
            py::arg("nominalTermStructure"),
            "Constructs with caplet vol and nominal term structure.")
        // Hidden handle constructors
        .def(py::init([](const ext::shared_ptr<YieldTermStructure>& yts) {
                return ext::make_shared<YoYInflationCouponPricer>(
                    Handle<YieldTermStructure>(yts));
            }),
            py::arg("nominalTermStructure"),
            "Constructs with a nominal term structure (handle created internally).")
        .def("capletVolatility", &YoYInflationCouponPricer::capletVolatility,
            "Returns the caplet volatility handle.")
        .def("nominalTermStructure",
            &YoYInflationCouponPricer::nominalTermStructure,
            "Returns the nominal term structure handle.")
        .def("setCapletVolatility",
            &YoYInflationCouponPricer::setCapletVolatility,
            py::arg("capletVol"),
            "Sets the caplet volatility handle.");

    // BlackYoYInflationCouponPricer
    py::class_<BlackYoYInflationCouponPricer, YoYInflationCouponPricer,
               ext::shared_ptr<BlackYoYInflationCouponPricer>>(
        m, "BlackYoYInflationCouponPricer",
        "Black-formula pricer for YoY inflation coupons.")
        .def(py::init<>(),
            "Constructs with no vol or nominal curve.")
        .def(py::init<const Handle<YieldTermStructure>&>(),
            py::arg("nominalTermStructure"),
            "Constructs with a nominal term structure.")
        .def(py::init<const Handle<YoYOptionletVolatilitySurface>&,
                       const Handle<YieldTermStructure>&>(),
            py::arg("capletVol"),
            py::arg("nominalTermStructure"),
            "Constructs with caplet vol and nominal term structure.");

    // UnitDisplacedBlackYoYInflationCouponPricer
    py::class_<UnitDisplacedBlackYoYInflationCouponPricer,
               YoYInflationCouponPricer,
               ext::shared_ptr<UnitDisplacedBlackYoYInflationCouponPricer>>(
        m, "UnitDisplacedBlackYoYInflationCouponPricer",
        "Unit-displaced Black pricer for YoY inflation coupons.")
        .def(py::init<>(),
            "Constructs with no vol or nominal curve.")
        .def(py::init<const Handle<YieldTermStructure>&>(),
            py::arg("nominalTermStructure"),
            "Constructs with a nominal term structure.")
        .def(py::init<const Handle<YoYOptionletVolatilitySurface>&,
                       const Handle<YieldTermStructure>&>(),
            py::arg("capletVol"),
            py::arg("nominalTermStructure"),
            "Constructs with caplet vol and nominal term structure.");

    // BachelierYoYInflationCouponPricer
    py::class_<BachelierYoYInflationCouponPricer, YoYInflationCouponPricer,
               ext::shared_ptr<BachelierYoYInflationCouponPricer>>(
        m, "BachelierYoYInflationCouponPricer",
        "Bachelier (normal) pricer for YoY inflation coupons.")
        .def(py::init<>(),
            "Constructs with no vol or nominal curve.")
        .def(py::init<const Handle<YieldTermStructure>&>(),
            py::arg("nominalTermStructure"),
            "Constructs with a nominal term structure.")
        .def(py::init<const Handle<YoYOptionletVolatilitySurface>&,
                       const Handle<YieldTermStructure>&>(),
            py::arg("capletVol"),
            py::arg("nominalTermStructure"),
            "Constructs with caplet vol and nominal term structure.");

    // setCouponPricer overload for inflation
    m.def("setCouponPricer",
        [](const Leg& leg,
           const ext::shared_ptr<InflationCouponPricer>& pricer) {
            setCouponPricer(leg, pricer);
        },
        py::arg("leg"), py::arg("pricer"),
        "Sets the coupon pricer for all inflation coupons in the leg.");
}
