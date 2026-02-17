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
#include <ql/pricingengines/inflation/inflationcapfloorengines.hpp>
#include <ql/indexes/inflationindex.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/termstructures/volatility/inflation/yoyinflationoptionletvolatilitystructure.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_pricingengines::inflationcapfloorengines(py::module_& m) {
    // YoYInflationBlackCapFloorEngine
    py::class_<YoYInflationBlackCapFloorEngine,
               PricingEngine,
               ext::shared_ptr<YoYInflationBlackCapFloorEngine>>(
        m, "YoYInflationBlackCapFloorEngine",
        "Black-formula engine for YoY inflation cap/floor.")
        .def(py::init<const ext::shared_ptr<YoYInflationIndex>&,
                       const Handle<YoYOptionletVolatilitySurface>&,
                       const Handle<YieldTermStructure>&>(),
            py::arg("index"),
            py::arg("volatility"),
            py::arg("nominalTermStructure"),
            "Constructs a Black YoY inflation cap/floor engine.")
        // Hidden handle constructors
        .def(py::init([](const ext::shared_ptr<YoYInflationIndex>& index,
                         const ext::shared_ptr<YoYOptionletVolatilitySurface>& vol,
                         const Handle<YieldTermStructure>& yts) {
                return ext::make_shared<YoYInflationBlackCapFloorEngine>(
                    index, Handle<YoYOptionletVolatilitySurface>(vol), yts);
            }),
            py::arg("index"),
            py::arg("volatility"),
            py::arg("nominalTermStructure"),
            "Constructs with vol surface (handle created internally).")
        .def(py::init([](const ext::shared_ptr<YoYInflationIndex>& index,
                         const Handle<YoYOptionletVolatilitySurface>& vol,
                         const ext::shared_ptr<YieldTermStructure>& yts) {
                return ext::make_shared<YoYInflationBlackCapFloorEngine>(
                    index, vol, Handle<YieldTermStructure>(yts));
            }),
            py::arg("index"),
            py::arg("volatility"),
            py::arg("nominalTermStructure"),
            "Constructs with nominal curve (handle created internally).")
        .def(py::init([](const ext::shared_ptr<YoYInflationIndex>& index,
                         const ext::shared_ptr<YoYOptionletVolatilitySurface>& vol,
                         const ext::shared_ptr<YieldTermStructure>& yts) {
                return ext::make_shared<YoYInflationBlackCapFloorEngine>(
                    index,
                    Handle<YoYOptionletVolatilitySurface>(vol),
                    Handle<YieldTermStructure>(yts));
            }),
            py::arg("index"),
            py::arg("volatility"),
            py::arg("nominalTermStructure"),
            "Constructs with both handles created internally.");

    // YoYInflationUnitDisplacedBlackCapFloorEngine
    py::class_<YoYInflationUnitDisplacedBlackCapFloorEngine,
               PricingEngine,
               ext::shared_ptr<YoYInflationUnitDisplacedBlackCapFloorEngine>>(
        m, "YoYInflationUnitDisplacedBlackCapFloorEngine",
        "Unit-displaced Black engine for YoY inflation cap/floor.")
        .def(py::init<const ext::shared_ptr<YoYInflationIndex>&,
                       const Handle<YoYOptionletVolatilitySurface>&,
                       const Handle<YieldTermStructure>&>(),
            py::arg("index"),
            py::arg("volatility"),
            py::arg("nominalTermStructure"),
            "Constructs a unit-displaced Black YoY inflation cap/floor engine.")
        .def(py::init([](const ext::shared_ptr<YoYInflationIndex>& index,
                         const ext::shared_ptr<YoYOptionletVolatilitySurface>& vol,
                         const ext::shared_ptr<YieldTermStructure>& yts) {
                return ext::make_shared<
                    YoYInflationUnitDisplacedBlackCapFloorEngine>(
                    index,
                    Handle<YoYOptionletVolatilitySurface>(vol),
                    Handle<YieldTermStructure>(yts));
            }),
            py::arg("index"),
            py::arg("volatility"),
            py::arg("nominalTermStructure"),
            "Constructs with both handles created internally.");

    // YoYInflationBachelierCapFloorEngine
    py::class_<YoYInflationBachelierCapFloorEngine,
               PricingEngine,
               ext::shared_ptr<YoYInflationBachelierCapFloorEngine>>(
        m, "YoYInflationBachelierCapFloorEngine",
        "Bachelier (normal) engine for YoY inflation cap/floor.")
        .def(py::init<const ext::shared_ptr<YoYInflationIndex>&,
                       const Handle<YoYOptionletVolatilitySurface>&,
                       const Handle<YieldTermStructure>&>(),
            py::arg("index"),
            py::arg("volatility"),
            py::arg("nominalTermStructure"),
            "Constructs a Bachelier YoY inflation cap/floor engine.")
        .def(py::init([](const ext::shared_ptr<YoYInflationIndex>& index,
                         const ext::shared_ptr<YoYOptionletVolatilitySurface>& vol,
                         const ext::shared_ptr<YieldTermStructure>& yts) {
                return ext::make_shared<
                    YoYInflationBachelierCapFloorEngine>(
                    index,
                    Handle<YoYOptionletVolatilitySurface>(vol),
                    Handle<YieldTermStructure>(yts));
            }),
            py::arg("index"),
            py::arg("volatility"),
            py::arg("nominalTermStructure"),
            "Constructs with both handles created internally.");
}
