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
#include "pyquantlib/trampolines.h"
#include <ql/instruments/swaption.hpp>
#include <ql/termstructures/yieldtermstructure.hpp>
#include <ql/termstructures/volatility/volatilitytype.hpp>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace QuantLib;

void ql_instruments::swaption(py::module_& m) {
    py::module_ base = m.def_submodule("base", "Abstract base classes");

    // Settlement::Type enum
    py::enum_<Settlement::Type>(m, "SettlementType",
        "Swaption settlement type.")
        .value("Physical", Settlement::Physical)
        .value("Cash", Settlement::Cash);

    // Settlement::Method enum
    py::enum_<Settlement::Method>(m, "SettlementMethod",
        "Swaption settlement method.")
        .value("PhysicalOTC", Settlement::PhysicalOTC)
        .value("PhysicalCleared", Settlement::PhysicalCleared)
        .value("CollateralizedCashPrice", Settlement::CollateralizedCashPrice)
        .value("ParYieldCurve", Settlement::ParYieldCurve);

    // Swaption::PriceType enum
    py::enum_<Swaption::PriceType>(m, "SwaptionPriceType",
        "Swaption price type for implied volatility.")
        .value("Spot", Swaption::Spot)
        .value("Forward", Swaption::Forward);

    // Swaption::arguments
    py::class_<Swaption::arguments, FixedVsFloatingSwap::arguments,
        Option::arguments, ext::shared_ptr<Swaption::arguments>>(
        m, "SwaptionArguments",
        "Arguments for swaption pricing.")
        .def(py::init<>())
        .def_readwrite("swap", &Swaption::arguments::swap)
        .def_readwrite("settlementType", &Swaption::arguments::settlementType)
        .def_readwrite("settlementMethod", &Swaption::arguments::settlementMethod)
        .def("validate", &Swaption::arguments::validate);

    // Swaption class
    auto pySwaption = py::class_<Swaption, Option, ext::shared_ptr<Swaption>>(
        m, "Swaption",
        "Option to enter into an interest rate swap.")
        .def(py::init<ext::shared_ptr<FixedVsFloatingSwap>,
                      const ext::shared_ptr<Exercise>&,
                      Settlement::Type, Settlement::Method>(),
            py::arg("swap"),
            py::arg("exercise"),
            py::arg("delivery") = Settlement::Physical,
            py::arg("settlementMethod") = Settlement::PhysicalOTC,
            "Constructs a swaption.")
        // Inspectors
        .def("settlementType", &Swaption::settlementType,
            "Returns the settlement type.")
        .def("settlementMethod", &Swaption::settlementMethod,
            "Returns the settlement method.")
        .def("type", &Swaption::type,
            "Returns the underlying swap type.")
        .def("underlying", &Swaption::underlying,
            "Returns the underlying swap.")
        .def("isExpired", &Swaption::isExpired,
            "Returns True if the swaption has expired.")
        // Implied volatility
        .def("impliedVolatility", &Swaption::impliedVolatility,
            py::arg("price"),
            py::arg("discountCurve"),
            py::arg("guess"),
            py::arg("accuracy") = 1.0e-4,
            py::arg("maxEvaluations") = 100,
            py::arg("minVol") = 1.0e-7,
            py::arg("maxVol") = 4.0,
            py::arg("type") = VolatilityType::ShiftedLognormal,
            py::arg("displacement") = 0.0,
            py::arg("priceType") = Swaption::Spot,
            "Returns the implied volatility.");

    // SwaptionGenericEngine base class
    py::class_<SwaptionGenericEngine, PySwaptionGenericEngine,
               ext::shared_ptr<SwaptionGenericEngine>, PricingEngine, Observer>(
        base, "SwaptionGenericEngine",
        "Generic base engine for swaptions.")
        .def(py::init_alias<>());

    // Swaption::engine
    py::class_<Swaption::engine, PySwaptionEngine,
               ext::shared_ptr<Swaption::engine>, SwaptionGenericEngine>(
        pySwaption, "engine",
        "Base class for swaption pricing engines.")
        .def(py::init_alias<>());
}
